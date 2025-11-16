"""
Base Agent SDK - Foundation for all platform agents.

All agents inherit from BaseAgent and get event bus, context access,
and lifecycle management for free.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Callable
from uuid import uuid4

from app.agent_platform.models.agent import (
    AgentCapability,
    AgentMetadata,
    AgentRegistration,
    AgentStatus,
)
from app.agent_platform.models.events import BaseEvent, EventPriority


class BaseAgent(ABC):
    """
    Base class for all platform agents.

    Provides:
    - Event bus integration (publish/subscribe)
    - Context graph access (query/update)
    - Lifecycle management (start/stop/health)
    - Automatic registration with agent registry
    - Performance monitoring
    """

    def __init__(
        self,
        name: str,
        description: str,
        version: str = "1.0.0",
        config: dict[str, Any] | None = None,
    ):
        """
        Initialize a new agent.

        Args:
            name: Unique name for this agent
            description: Human-readable description
            version: Semantic version
            config: Optional configuration dictionary
        """
        self.agent_id = str(uuid4())
        self.name = name
        self.description = description
        self.version = version
        self.config = config or {}

        # Runtime state
        self.status = AgentStatus.INITIALIZING
        self.start_time: datetime | None = None
        self.event_handlers: dict[str, list[Callable]] = {}
        self.metadata = AgentMetadata(
            agent_id=self.agent_id,
            name=name,
            version=version,
            description=description,
            config=self.config,
        )

        # Will be injected by platform
        self.event_bus = None
        self.context_service = None
        self.registry = None

        # Logging
        self.logger = logging.getLogger(f"agent.{name}")

    # -------------------------------------------------------------------------
    # Lifecycle Methods (Override as needed)
    # -------------------------------------------------------------------------

    async def setup(self) -> None:
        """
        Setup hook called before agent starts.

        Override this to initialize resources, load models, etc.
        """
        pass

    async def teardown(self) -> None:
        """
        Teardown hook called when agent stops.

        Override this to cleanup resources, save state, etc.
        """
        pass

    @abstractmethod
    async def process_event(self, event: BaseEvent) -> None:
        """
        Process an incoming event.

        This is the main entry point for agent logic. Override this
        to define how your agent responds to events.

        Args:
            event: The event to process
        """
        pass

    async def health_check(self) -> dict[str, Any]:
        """
        Perform a health check.

        Override to add custom health metrics.

        Returns:
            Dictionary with health status and metrics
        """
        return {
            "status": "healthy" if self.status == AgentStatus.RUNNING else "unhealthy",
            "agent_id": self.agent_id,
            "name": self.name,
            "uptime_seconds": self.get_uptime(),
            "events_processed": self.metadata.total_events_processed,
        }

    # -------------------------------------------------------------------------
    # Event Bus Integration
    # -------------------------------------------------------------------------

    async def publish_event(
        self,
        event_type: str,
        data: dict[str, Any],
        priority: EventPriority = EventPriority.NORMAL,
        correlation_id: str | None = None,
    ) -> None:
        """
        Publish an event to the event bus.

        Args:
            event_type: Type of event (e.g., "task.completed")
            data: Event payload
            priority: Event priority level
            correlation_id: Optional ID to correlate related events
        """
        if not self.event_bus:
            self.logger.warning("Event bus not available, event not published")
            return

        event = BaseEvent(
            event_type=event_type,
            source_agent=self.name,
            data=data,
            priority=priority,
            correlation_id=correlation_id,
        )

        await self.event_bus.publish(event)
        self.metadata.total_events_published += 1

    async def subscribe(self, pattern: str, handler: Callable) -> None:
        """
        Subscribe to events matching a pattern.

        Args:
            pattern: Event pattern (e.g., "task.*", "agent.registered")
            handler: Async function to handle matching events
        """
        if pattern not in self.event_handlers:
            self.event_handlers[pattern] = []

        self.event_handlers[pattern].append(handler)

        if self.event_bus:
            await self.event_bus.subscribe(pattern, self._handle_event_wrapper)

        self.metadata.subscribes_to.append(pattern)

    async def _handle_event_wrapper(self, event: BaseEvent) -> None:
        """Internal wrapper that tracks metrics and calls user handler."""
        start_time = asyncio.get_event_loop().time()

        try:
            await self.process_event(event)
            self.metadata.total_events_processed += 1

            # Update average response time
            elapsed_ms = (asyncio.get_event_loop().time() - start_time) * 1000
            n = self.metadata.total_events_processed
            self.metadata.average_response_time_ms = (
                self.metadata.average_response_time_ms * (n - 1) + elapsed_ms
            ) / n

        except Exception as e:
            self.logger.error(f"Error processing event: {e}", exc_info=True)
            self.metadata.error_count += 1
            await self._handle_error(event, e)

    async def _handle_error(self, event: BaseEvent, error: Exception) -> None:
        """Handle errors during event processing."""
        await self.publish_event(
            event_type="agent.error",
            data={
                "error": str(error),
                "error_type": type(error).__name__,
                "failed_event": event.model_dump(),
            },
            priority=EventPriority.HIGH,
        )

    # -------------------------------------------------------------------------
    # Context Graph Integration
    # -------------------------------------------------------------------------

    async def query_context(
        self, query: str, parameters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Query the context graph using Cypher.

        Args:
            query: Cypher query string
            parameters: Query parameters

        Returns:
            List of result records
        """
        if not self.context_service:
            self.logger.warning("Context service not available")
            return []

        return await self.context_service.query(query, parameters or {})

    async def update_context(
        self, node_type: str, properties: dict[str, Any], node_id: str | None = None
    ) -> str:
        """
        Create or update a context node.

        Args:
            node_type: Type of node (e.g., "health", "task")
            properties: Node properties
            node_id: Optional node ID (creates new if not provided)

        Returns:
            The node ID
        """
        if not self.context_service:
            self.logger.warning("Context service not available")
            return ""

        return await self.context_service.update_node(node_type, properties, node_id)

    async def create_relationship(
        self, from_node: str, to_node: str, rel_type: str, properties: dict | None = None
    ) -> None:
        """
        Create a relationship between context nodes.

        Args:
            from_node: Source node ID
            to_node: Target node ID
            rel_type: Relationship type
            properties: Optional relationship properties
        """
        if not self.context_service:
            self.logger.warning("Context service not available")
            return

        await self.context_service.create_relationship(
            from_node, to_node, rel_type, properties or {}
        )

    # -------------------------------------------------------------------------
    # Lifecycle Management
    # -------------------------------------------------------------------------

    async def start(self) -> None:
        """Start the agent."""
        self.logger.info(f"Starting agent: {self.name}")
        self.status = AgentStatus.RUNNING
        self.start_time = datetime.now(timezone.utc)

        await self.setup()
        await self._register()
        await self.publish_event("agent.started", {"agent_id": self.agent_id})

    async def stop(self) -> None:
        """Stop the agent."""
        self.logger.info(f"Stopping agent: {self.name}")
        self.status = AgentStatus.STOPPED

        await self.publish_event("agent.stopped", {"agent_id": self.agent_id})
        await self.teardown()

    async def _register(self) -> None:
        """Register with the agent registry."""
        if not self.registry:
            self.logger.warning("Registry not available, skipping registration")
            return

        registration = AgentRegistration(
            name=self.name,
            description=self.description,
            capabilities=self.get_capabilities(),
            subscribes_to=self.metadata.subscribes_to,
            publishes=self.metadata.publishes,
            provides_context=self.metadata.provides_context,
            config=self.config,
        )

        await self.registry.register(registration, self)

    # -------------------------------------------------------------------------
    # Agent Capabilities (Override to declare what your agent can do)
    # -------------------------------------------------------------------------

    def get_capabilities(self) -> list[AgentCapability]:
        """
        Return list of capabilities this agent provides.

        Override this to declare your agent's capabilities.

        Returns:
            List of AgentCapability objects
        """
        return []

    # -------------------------------------------------------------------------
    # Utilities
    # -------------------------------------------------------------------------

    def get_uptime(self) -> float:
        """Get agent uptime in seconds."""
        if not self.start_time:
            return 0.0
        return (datetime.now(timezone.utc) - self.start_time).total_seconds()

    async def send_notification(self, message: str, priority: EventPriority = EventPriority.NORMAL) -> None:
        """Send a user notification."""
        await self.publish_event(
            "user.notification",
            {"message": message, "agent": self.name},
            priority=priority,
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name}, status={self.status})>"
