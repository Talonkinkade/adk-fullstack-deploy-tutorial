"""
Agent metadata and capability models.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    """Status of an agent in the platform."""

    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    STOPPED = "stopped"


class AgentCapability(BaseModel):
    """A capability that an agent provides."""

    name: str
    description: str
    input_schema: dict[str, Any] | None = None
    output_schema: dict[str, Any] | None = None
    required_context: list[str] = Field(default_factory=list)


class AgentDependency(BaseModel):
    """A dependency on another agent or service."""

    type: str  # "agent", "service", "data_source"
    name: str
    required: bool = True
    version: str | None = None


class AgentMetadata(BaseModel):
    """Complete metadata about an agent."""

    # Identity
    agent_id: str
    name: str
    version: str = "1.0.0"
    description: str

    # Capabilities
    capabilities: list[AgentCapability] = Field(default_factory=list)
    subscribes_to: list[str] = Field(default_factory=list)  # Event patterns
    publishes: list[str] = Field(default_factory=list)  # Event types
    provides_context: list[str] = Field(default_factory=list)  # Context types

    # Dependencies
    dependencies: list[AgentDependency] = Field(default_factory=list)

    # Runtime info
    status: AgentStatus = AgentStatus.INITIALIZING
    health_score: float = 1.0  # 0.0 to 1.0
    last_heartbeat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Configuration
    config: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)

    # Metrics
    total_events_processed: int = 0
    total_events_published: int = 0
    average_response_time_ms: float = 0.0
    error_count: int = 0
    uptime_seconds: float = 0.0

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class AgentRegistration(BaseModel):
    """Request to register an agent with the platform."""

    name: str
    description: str
    capabilities: list[AgentCapability] = Field(default_factory=list)
    subscribes_to: list[str] = Field(default_factory=list)
    publishes: list[str] = Field(default_factory=list)
    provides_context: list[str] = Field(default_factory=list)
    dependencies: list[AgentDependency] = Field(default_factory=list)
    config: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
