"""
Event models for the agent platform.

All agents communicate via typed events through the event bus.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class EventPriority(str, Enum):
    """Priority levels for events."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class EventType(str, Enum):
    """Standard event types across the platform."""

    # Agent lifecycle events
    AGENT_REGISTERED = "agent.registered"
    AGENT_STARTED = "agent.started"
    AGENT_STOPPED = "agent.stopped"
    AGENT_ERROR = "agent.error"

    # Task and workflow events
    TASK_CREATED = "task.created"
    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"

    # Context events
    CONTEXT_UPDATED = "context.updated"
    CONTEXT_QUERY = "context.query"

    # Data events
    DATA_COLLECTED = "data.collected"
    INSIGHT_GENERATED = "insight.generated"
    PATTERN_DETECTED = "pattern.detected"

    # User interaction events
    USER_INPUT = "user.input"
    USER_NOTIFICATION = "user.notification"

    # Health and performance events
    HEALTH_CHECK = "health.check"
    PERFORMANCE_METRIC = "performance.metric"
    ANOMALY_DETECTED = "anomaly.detected"

    # Custom event type
    CUSTOM = "custom"


class BaseEvent(BaseModel):
    """Base event model that all platform events inherit from."""

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str
    source_agent: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    priority: EventPriority = EventPriority.NORMAL
    data: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    correlation_id: str | None = None  # For tracking related events
    causation_id: str | None = None  # The event that caused this one

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class AgentEvent(BaseEvent):
    """Events specific to agent lifecycle and operations."""

    agent_name: str
    agent_status: str | None = None


class TaskEvent(BaseEvent):
    """Events related to task execution."""

    task_id: str
    task_name: str
    task_status: str
    progress: float = 0.0  # 0.0 to 1.0


class ContextEvent(BaseEvent):
    """Events related to context updates and queries."""

    context_type: str  # e.g., "health", "finance", "project"
    context_data: dict[str, Any]
    affected_entities: list[str] = Field(default_factory=list)


class DataEvent(BaseEvent):
    """Events for data collection and insights."""

    data_type: str
    data_source: str
    data_payload: dict[str, Any]
    confidence: float | None = None  # For ML-generated insights


class PerformanceEvent(BaseEvent):
    """Events for performance monitoring."""

    metric_name: str
    metric_value: float
    metric_unit: str
    agent_name: str
    threshold_exceeded: bool = False
