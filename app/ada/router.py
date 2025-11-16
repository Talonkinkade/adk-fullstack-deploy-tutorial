"""Request Router - Intelligent routing of requests to appropriate agents.

Routes requests based on:
- Request type and capabilities needed
- Agent availability and current load
- Priority and SLA requirements
- Performance history
"""

import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Any

from .registry import (
    AgentRegistry,
    AgentManifest,
    AgentCapability,
    AgentTier,
)


class RequestPriority(Enum):
    """Request priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class RequestType(Enum):
    """Types of requests that can be routed."""
    GOAL_PLANNING = "goal_planning"
    TASK_DECOMPOSITION = "task_decomposition"
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    DATA_PROCESSING = "data_processing"
    ANALYTICS = "analytics"
    MONITORING = "monitoring"
    DOCUMENTATION = "documentation"


# Mapping of request types to required capabilities
REQUEST_CAPABILITY_MAP: Dict[RequestType, AgentCapability] = {
    RequestType.GOAL_PLANNING: AgentCapability.PLANNING,
    RequestType.TASK_DECOMPOSITION: AgentCapability.PLANNING,
    RequestType.CODE_GENERATION: AgentCapability.CODE_GENERATION,
    RequestType.CODE_REVIEW: AgentCapability.CODE_REVIEW,
    RequestType.TESTING: AgentCapability.TESTING,
    RequestType.DEPLOYMENT: AgentCapability.DEPLOYMENT,
    RequestType.DATA_PROCESSING: AgentCapability.DATA_PROCESSING,
    RequestType.ANALYTICS: AgentCapability.ANALYTICS,
    RequestType.MONITORING: AgentCapability.MONITORING,
    RequestType.DOCUMENTATION: AgentCapability.DOCUMENTATION,
}


@dataclass
class RoutingRequest:
    """Request to be routed to an agent."""
    request_id: str
    request_type: RequestType
    priority: RequestPriority = RequestPriority.NORMAL
    payload: Dict[str, Any] = None
    preferred_tier: Optional[AgentTier] = None
    preferred_agent_id: Optional[str] = None
    timeout_seconds: int = 300
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.payload is None:
            self.payload = {}


@dataclass
class RoutingResult:
    """Result of routing decision."""
    success: bool
    agent: Optional[AgentManifest] = None
    error: Optional[str] = None
    routing_time_ms: float = 0.0


class RoutingStrategy(Enum):
    """Agent selection strategies."""
    ROUND_ROBIN = "round_robin"
    LEAST_LOADED = "least_loaded"
    BEST_PERFORMANCE = "best_performance"
    RANDOM = "random"


class RequestRouter:
    """Route requests to appropriate agents based on multiple factors.

    Features:
    - Capability-based routing
    - Load balancing
    - Performance-aware selection
    - Priority queue support
    """

    def __init__(
        self,
        registry: AgentRegistry,
        default_strategy: RoutingStrategy = RoutingStrategy.LEAST_LOADED
    ):
        """Initialize request router.

        Args:
            registry: Agent registry for discovering agents
            default_strategy: Default routing strategy
        """
        self.registry = registry
        self.default_strategy = default_strategy

        # Round-robin counters for each capability
        self._round_robin_counters: Dict[AgentCapability, int] = {}

    def route(
        self,
        request: RoutingRequest,
        strategy: Optional[RoutingStrategy] = None
    ) -> RoutingResult:
        """Route a request to an appropriate agent.

        Args:
            request: Request to route
            strategy: Routing strategy (uses default if None)

        Returns:
            RoutingResult with selected agent or error
        """
        start_time = time.time()
        strategy = strategy or self.default_strategy

        # Check if specific agent requested
        if request.preferred_agent_id:
            agent = self.registry.get(request.preferred_agent_id)
            if agent and agent.is_available:
                return RoutingResult(
                    success=True,
                    agent=agent,
                    routing_time_ms=(time.time() - start_time) * 1000
                )
            return RoutingResult(
                success=False,
                error=f"Preferred agent {request.preferred_agent_id} not available"
            )

        # Get required capability
        required_capability = REQUEST_CAPABILITY_MAP.get(request.request_type)
        if not required_capability:
            return RoutingResult(
                success=False,
                error=f"Unknown request type: {request.request_type}"
            )

        # Find available agents with capability
        candidates = self.registry.find_available(
            capability=required_capability,
            tier=request.preferred_tier
        )

        if not candidates:
            return RoutingResult(
                success=False,
                error=f"No available agents with capability {required_capability.value}"
            )

        # Select agent based on strategy
        selected = self._select_agent(candidates, strategy, required_capability)

        if not selected:
            return RoutingResult(
                success=False,
                error="Failed to select agent from candidates"
            )

        return RoutingResult(
            success=True,
            agent=selected,
            routing_time_ms=(time.time() - start_time) * 1000
        )

    def _select_agent(
        self,
        candidates: List[AgentManifest],
        strategy: RoutingStrategy,
        capability: AgentCapability
    ) -> Optional[AgentManifest]:
        """Select an agent from candidates based on strategy."""

        if not candidates:
            return None

        if strategy == RoutingStrategy.LEAST_LOADED:
            # Already sorted by load in registry.find_available()
            return candidates[0]

        elif strategy == RoutingStrategy.BEST_PERFORMANCE:
            # Sort by success rate (descending) then response time (ascending)
            candidates.sort(
                key=lambda a: (-a.success_rate, a.avg_response_time_ms)
            )
            return candidates[0]

        elif strategy == RoutingStrategy.ROUND_ROBIN:
            # Get counter for this capability
            counter = self._round_robin_counters.get(capability, 0)
            selected = candidates[counter % len(candidates)]
            self._round_robin_counters[capability] = counter + 1
            return selected

        elif strategy == RoutingStrategy.RANDOM:
            import random
            return random.choice(candidates)

        return candidates[0]

    def get_routing_statistics(self) -> dict:
        """Get routing statistics."""
        stats = {
            "total_agents": len(self.registry.agents),
            "available_agents": len([
                a for a in self.registry.agents.values()
                if a.is_available
            ]),
            "by_capability": {},
            "by_tier": {},
        }

        # Count available agents by capability
        for capability in AgentCapability:
            available = len(self.registry.find_available(capability=capability))
            stats["by_capability"][capability.value] = available

        # Count available agents by tier
        for tier in AgentTier:
            available = len(self.registry.find_available(tier=tier))
            stats["by_tier"][f"tier_{tier.value}"] = available

        return stats

    def can_route(self, request_type: RequestType) -> bool:
        """Check if a request type can be routed.

        Args:
            request_type: Type of request

        Returns:
            True if at least one agent available for this request type
        """
        required_capability = REQUEST_CAPABILITY_MAP.get(request_type)
        if not required_capability:
            return False

        candidates = self.registry.find_available(capability=required_capability)
        return len(candidates) > 0
