"""
Event Bus - Message broker for agent communication.

Supports Redis Streams for high-throughput event distribution.
Includes pattern matching, priorities, and replay capabilities.
"""

import asyncio
import json
import logging
import re
from datetime import datetime, timezone
from typing import Any, Callable

from app.agent_platform.models.events import BaseEvent, EventPriority

logger = logging.getLogger(__name__)


class EventBus:
    """
    Async event bus for agent communication.

    Features:
    - Pattern-based subscriptions (e.g., "task.*", "agent.started")
    - Priority queues
    - Event replay (read past events)
    - Correlation/causation tracking
    - Dead letter queue for failed events
    """

    def __init__(self, redis_client: Any | None = None):
        """
        Initialize event bus.

        Args:
            redis_client: Optional Redis client (uses in-memory if None)
        """
        self.redis = redis_client
        self.subscribers: dict[str, list[Callable]] = {}
        self.in_memory_events: list[BaseEvent] = []
        self.running = False
        self._consumer_tasks: list[asyncio.Task] = []

    # -------------------------------------------------------------------------
    # Publish Events
    # -------------------------------------------------------------------------

    async def publish(self, event: BaseEvent) -> None:
        """
        Publish an event to the bus.

        Args:
            event: Event to publish
        """
        logger.debug(f"Publishing event: {event.event_type} from {event.source_agent}")

        if self.redis:
            await self._publish_to_redis(event)
        else:
            await self._publish_in_memory(event)

    async def _publish_to_redis(self, event: BaseEvent) -> None:
        """Publish event to Redis stream."""
        stream_name = f"events:{event.priority.value}"

        await self.redis.xadd(
            stream_name,
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "source_agent": event.source_agent,
                "timestamp": event.timestamp.isoformat(),
                "data": json.dumps(event.data),
                "metadata": json.dumps(event.metadata),
                "correlation_id": event.correlation_id or "",
                "causation_id": event.causation_id or "",
            },
        )

    async def _publish_in_memory(self, event: BaseEvent) -> None:
        """Publish event to in-memory queue."""
        self.in_memory_events.append(event)

        # Notify subscribers
        for pattern, handlers in self.subscribers.items():
            if self._pattern_matches(pattern, event.event_type):
                for handler in handlers:
                    try:
                        await handler(event)
                    except Exception as e:
                        logger.error(
                            f"Error in event handler for {pattern}: {e}", exc_info=True
                        )

    # -------------------------------------------------------------------------
    # Subscribe to Events
    # -------------------------------------------------------------------------

    async def subscribe(
        self, pattern: str, handler: Callable[[BaseEvent], None]
    ) -> None:
        """
        Subscribe to events matching a pattern.

        Args:
            pattern: Event pattern (supports wildcards: "task.*", "*.created")
            handler: Async function to call when event matches
        """
        logger.info(f"Subscribing to pattern: {pattern}")

        if pattern not in self.subscribers:
            self.subscribers[pattern] = []

        self.subscribers[pattern].append(handler)

        # Start consumer if using Redis
        if self.redis and self.running:
            task = asyncio.create_task(self._consume_from_redis(pattern))
            self._consumer_tasks.append(task)

    async def unsubscribe(self, pattern: str, handler: Callable) -> None:
        """Remove a subscription."""
        if pattern in self.subscribers:
            self.subscribers[pattern].remove(handler)
            if not self.subscribers[pattern]:
                del self.subscribers[pattern]

    # -------------------------------------------------------------------------
    # Pattern Matching
    # -------------------------------------------------------------------------

    @staticmethod
    def _pattern_matches(pattern: str, event_type: str) -> bool:
        """
        Check if event type matches subscription pattern.

        Supports:
        - Exact match: "task.created"
        - Wildcard suffix: "task.*"
        - Wildcard prefix: "*.created"
        - Full wildcard: "*"

        Args:
            pattern: Subscription pattern
            event_type: Event type to check

        Returns:
            True if event type matches pattern
        """
        if pattern == "*":
            return True

        # Convert glob pattern to regex
        regex_pattern = pattern.replace(".", r"\.").replace("*", ".*")
        return bool(re.match(f"^{regex_pattern}$", event_type))

    # -------------------------------------------------------------------------
    # Redis Consumer (for distributed mode)
    # -------------------------------------------------------------------------

    async def _consume_from_redis(self, pattern: str) -> None:
        """Consume events from Redis streams."""
        consumer_group = f"consumer_group_{pattern.replace('.', '_').replace('*', 'all')}"
        consumer_name = f"consumer_{id(self)}"

        # Create consumer group if it doesn't exist
        for priority in EventPriority:
            stream_name = f"events:{priority.value}"
            try:
                await self.redis.xgroup_create(
                    stream_name, consumer_group, id="0", mkstream=True
                )
            except Exception:
                pass  # Group already exists

        while self.running:
            try:
                # Read from all priority streams
                streams = {
                    f"events:{priority.value}": ">"
                    for priority in [
                        EventPriority.CRITICAL,
                        EventPriority.HIGH,
                        EventPriority.NORMAL,
                        EventPriority.LOW,
                    ]
                }

                events = await self.redis.xreadgroup(
                    consumer_group,
                    consumer_name,
                    streams,
                    count=10,
                    block=1000,  # 1 second
                )

                if events:
                    for stream_name, messages in events:
                        for message_id, data in messages:
                            event = self._deserialize_event(data)

                            # Check if event matches our pattern
                            if self._pattern_matches(pattern, event.event_type):
                                for handler in self.subscribers.get(pattern, []):
                                    try:
                                        await handler(event)
                                        # Acknowledge message
                                        await self.redis.xack(
                                            stream_name, consumer_group, message_id
                                        )
                                    except Exception as e:
                                        logger.error(
                                            f"Error processing event: {e}", exc_info=True
                                        )

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Redis consumer: {e}", exc_info=True)
                await asyncio.sleep(1)

    @staticmethod
    def _deserialize_event(data: dict[str, str]) -> BaseEvent:
        """Deserialize event from Redis."""
        return BaseEvent(
            event_id=data["event_id"],
            event_type=data["event_type"],
            source_agent=data["source_agent"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            priority=EventPriority(data.get("priority", "normal")),
            data=json.loads(data["data"]),
            metadata=json.loads(data["metadata"]),
            correlation_id=data.get("correlation_id") or None,
            causation_id=data.get("causation_id") or None,
        )

    # -------------------------------------------------------------------------
    # Event Replay & Query
    # -------------------------------------------------------------------------

    async def replay_events(
        self,
        pattern: str | None = None,
        since: datetime | None = None,
        limit: int = 100,
    ) -> list[BaseEvent]:
        """
        Replay past events (useful for agent initialization).

        Args:
            pattern: Optional event type pattern to filter
            since: Only return events after this timestamp
            limit: Maximum number of events to return

        Returns:
            List of historical events
        """
        if self.redis:
            # Read from Redis streams
            events = []
            for priority in EventPriority:
                stream_name = f"events:{priority.value}"
                results = await self.redis.xrange(stream_name, "-", "+", count=limit)

                for _, data in results:
                    event = self._deserialize_event(data)

                    # Apply filters
                    if pattern and not self._pattern_matches(pattern, event.event_type):
                        continue
                    if since and event.timestamp < since:
                        continue

                    events.append(event)

            # Sort by timestamp and limit
            events.sort(key=lambda e: e.timestamp)
            return events[:limit]

        else:
            # Filter in-memory events
            events = self.in_memory_events

            if pattern:
                events = [
                    e for e in events if self._pattern_matches(pattern, e.event_type)
                ]
            if since:
                events = [e for e in events if e.timestamp >= since]

            return events[-limit:]

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    async def start(self) -> None:
        """Start the event bus."""
        logger.info("Starting event bus")
        self.running = True

    async def stop(self) -> None:
        """Stop the event bus and cleanup."""
        logger.info("Stopping event bus")
        self.running = False

        # Cancel all consumer tasks
        for task in self._consumer_tasks:
            task.cancel()

        await asyncio.gather(*self._consumer_tasks, return_exceptions=True)
        self._consumer_tasks.clear()

    # -------------------------------------------------------------------------
    # Utilities
    # -------------------------------------------------------------------------

    async def get_stats(self) -> dict[str, Any]:
        """Get event bus statistics."""
        stats = {
            "total_subscribers": sum(len(handlers) for handlers in self.subscribers.values()),
            "subscription_patterns": list(self.subscribers.keys()),
            "mode": "redis" if self.redis else "in_memory",
        }

        if not self.redis:
            stats["in_memory_events"] = len(self.in_memory_events)

        return stats
