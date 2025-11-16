"""Agent performance metrics schemas."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class AgentMetrics:
    """Core agent performance metrics."""
    agent_id: str
    agent_name: str
    tier: int

    # Task metrics
    total_tasks: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0

    # Performance metrics
    avg_response_time_ms: float = 0.0
    min_response_time_ms: float = 0.0
    max_response_time_ms: float = 0.0

    # Availability
    uptime_percentage: float = 100.0
    current_load: int = 0
    max_load: int = 1

    # Calculated metrics
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_tasks == 0:
            return 0.0
        return (self.successful_tasks / self.total_tasks) * 100

    @property
    def failure_rate(self) -> float:
        """Calculate failure rate percentage."""
        return 100.0 - self.success_rate

    @property
    def load_percentage(self) -> float:
        """Calculate current load as percentage of max."""
        if self.max_load == 0:
            return 0.0
        return (self.current_load / self.max_load) * 100

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "tier": self.tier,
            "total_tasks": self.total_tasks,
            "successful_tasks": self.successful_tasks,
            "failed_tasks": self.failed_tasks,
            "success_rate": round(self.success_rate, 2),
            "failure_rate": round(self.failure_rate, 2),
            "avg_response_time_ms": round(self.avg_response_time_ms, 2),
            "min_response_time_ms": round(self.min_response_time_ms, 2),
            "max_response_time_ms": round(self.max_response_time_ms, 2),
            "uptime_percentage": round(self.uptime_percentage, 2),
            "current_load": self.current_load,
            "max_load": self.max_load,
            "load_percentage": round(self.load_percentage, 2),
        }


@dataclass
class PerformanceMetrics:
    """Extended performance metrics with trends."""
    agent_id: str
    timestamp: datetime

    # Core metrics
    metrics: AgentMetrics

    # Trend indicators
    success_rate_trend: Optional[str] = None  # "improving", "stable", "declining"
    response_time_trend: Optional[str] = None

    # Comparisons
    percentile_rank: Optional[float] = None  # 0-100
    tier_rank: Optional[int] = None

    # Additional context
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "timestamp": self.timestamp.isoformat(),
            "metrics": self.metrics.to_dict(),
            "success_rate_trend": self.success_rate_trend,
            "response_time_trend": self.response_time_trend,
            "percentile_rank": self.percentile_rank,
            "tier_rank": self.tier_rank,
            "metadata": self.metadata,
        }
