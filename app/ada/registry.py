"""Agent Registry - Central agent registration and discovery system.

Manages the lifecycle and metadata of all agents in the LearnQwest ecosystem.
"""

import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set


class AgentStatus(Enum):
    """Agent operational status."""
    INITIALIZING = "initializing"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class AgentTier(Enum):
    """8-tier hierarchy levels."""
    TIER_1_ORCHESTRATION = 1
    TIER_2_STRATEGIC = 2
    TIER_3_COORDINATORS = 3
    TIER_4_WORKERS = 4
    TIER_5_DATA = 5
    TIER_6_INTELLIGENCE = 6
    TIER_7_INTEGRATION = 7
    TIER_8_PRESENTATION = 8


class AgentCapability(Enum):
    """Agent capability tags."""
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    DATA_PROCESSING = "data_processing"
    ANALYTICS = "analytics"
    MONITORING = "monitoring"
    DOCUMENTATION = "documentation"
    ORCHESTRATION = "orchestration"
    PLANNING = "planning"


@dataclass
class AgentManifest:
    """Agent registration manifest with metadata."""

    # Identity
    agent_id: str
    name: str
    description: str
    tier: AgentTier

    # Capabilities
    capabilities: Set[AgentCapability] = field(default_factory=set)

    # Configuration
    model: str = "gemini-2.5-flash"
    max_concurrent_tasks: int = 1
    timeout_seconds: int = 300

    # Runtime state
    status: AgentStatus = AgentStatus.INITIALIZING
    current_load: int = 0  # Number of active tasks

    # Metadata
    created_at: float = field(default_factory=time.time)
    last_heartbeat: float = field(default_factory=time.time)
    version: str = "1.0.0"

    # Performance metrics
    total_tasks: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    avg_response_time_ms: float = 0.0

    # Dependencies
    depends_on: List[str] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)

    @property
    def success_rate(self) -> float:
        """Calculate task success rate."""
        if self.total_tasks == 0:
            return 0.0
        return (self.successful_tasks / self.total_tasks) * 100

    @property
    def is_available(self) -> bool:
        """Check if agent can accept new tasks."""
        return (
            self.status == AgentStatus.READY and
            self.current_load < self.max_concurrent_tasks
        )

    @property
    def is_healthy(self) -> bool:
        """Check if agent is responding (heartbeat within 60s)."""
        return (time.time() - self.last_heartbeat) < 60

    def heartbeat(self) -> None:
        """Update last heartbeat timestamp."""
        self.last_heartbeat = time.time()

    def increment_load(self) -> None:
        """Mark agent as handling a new task."""
        self.current_load += 1
        self.total_tasks += 1
        if self.current_load >= self.max_concurrent_tasks:
            self.status = AgentStatus.BUSY

    def decrement_load(self, success: bool = True, response_time_ms: float = 0) -> None:
        """Mark task completion and update metrics."""
        if self.current_load > 0:
            self.current_load -= 1

        if success:
            self.successful_tasks += 1
        else:
            self.failed_tasks += 1

        # Update rolling average response time
        if self.total_tasks > 0:
            self.avg_response_time_ms = (
                (self.avg_response_time_ms * (self.total_tasks - 1) + response_time_ms) /
                self.total_tasks
            )

        if self.current_load < self.max_concurrent_tasks:
            self.status = AgentStatus.READY

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        data = asdict(self)
        # Convert enums and sets to serializable types
        data['tier'] = self.tier.value
        data['status'] = self.status.value
        data['capabilities'] = [c.value for c in self.capabilities]
        data['tags'] = list(self.tags)
        return data


class AgentRegistry:
    """Central registry for all agents in the system.

    Provides:
    - Agent registration and deregistration
    - Agent discovery by capability, tier, or tags
    - Health monitoring and status tracking
    - Persistence to disk
    """

    def __init__(self, registry_path: Optional[Path] = None):
        """Initialize agent registry.

        Args:
            registry_path: Path to persist registry data (JSON file)
        """
        self.agents: Dict[str, AgentManifest] = {}
        self.registry_path = registry_path or Path("config/agent_registry.json")
        self._load_registry()

    def register(self, manifest: AgentManifest) -> bool:
        """Register a new agent.

        Args:
            manifest: Agent manifest with metadata

        Returns:
            True if registration successful, False if agent already exists
        """
        if manifest.agent_id in self.agents:
            return False

        self.agents[manifest.agent_id] = manifest
        self._persist_registry()
        return True

    def deregister(self, agent_id: str) -> bool:
        """Deregister an agent.

        Args:
            agent_id: Unique agent identifier

        Returns:
            True if deregistration successful, False if agent not found
        """
        if agent_id not in self.agents:
            return False

        del self.agents[agent_id]
        self._persist_registry()
        return True

    def get(self, agent_id: str) -> Optional[AgentManifest]:
        """Get agent manifest by ID."""
        return self.agents.get(agent_id)

    def update_status(self, agent_id: str, status: AgentStatus) -> bool:
        """Update agent status.

        Args:
            agent_id: Agent to update
            status: New status

        Returns:
            True if update successful
        """
        agent = self.agents.get(agent_id)
        if not agent:
            return False

        agent.status = status
        self._persist_registry()
        return True

    def heartbeat(self, agent_id: str) -> bool:
        """Record agent heartbeat.

        Args:
            agent_id: Agent sending heartbeat

        Returns:
            True if heartbeat recorded
        """
        agent = self.agents.get(agent_id)
        if not agent:
            return False

        agent.heartbeat()
        return True

    def find_by_capability(self, capability: AgentCapability) -> List[AgentManifest]:
        """Find all agents with a specific capability."""
        return [
            agent for agent in self.agents.values()
            if capability in agent.capabilities
        ]

    def find_by_tier(self, tier: AgentTier) -> List[AgentManifest]:
        """Find all agents in a specific tier."""
        return [
            agent for agent in self.agents.values()
            if agent.tier == tier
        ]

    def find_by_tag(self, tag: str) -> List[AgentManifest]:
        """Find all agents with a specific tag."""
        return [
            agent for agent in self.agents.values()
            if tag in agent.tags
        ]

    def find_available(
        self,
        capability: Optional[AgentCapability] = None,
        tier: Optional[AgentTier] = None
    ) -> List[AgentManifest]:
        """Find available agents matching criteria.

        Args:
            capability: Filter by capability (optional)
            tier: Filter by tier (optional)

        Returns:
            List of available agents matching criteria
        """
        candidates = list(self.agents.values())

        # Filter by availability first
        candidates = [a for a in candidates if a.is_available]

        # Apply filters
        if capability:
            candidates = [a for a in candidates if capability in a.capabilities]
        if tier:
            candidates = [a for a in candidates if a.tier == tier]

        # Sort by current load (prefer less loaded agents)
        candidates.sort(key=lambda a: a.current_load)

        return candidates

    def get_unhealthy_agents(self) -> List[AgentManifest]:
        """Find agents that haven't sent heartbeat recently."""
        return [
            agent for agent in self.agents.values()
            if not agent.is_healthy
        ]

    def get_statistics(self) -> dict:
        """Get registry statistics."""
        total = len(self.agents)
        by_status = {}
        by_tier = {}

        for agent in self.agents.values():
            # Count by status
            status_key = agent.status.value
            by_status[status_key] = by_status.get(status_key, 0) + 1

            # Count by tier
            tier_key = f"tier_{agent.tier.value}"
            by_tier[tier_key] = by_tier.get(tier_key, 0) + 1

        available = len([a for a in self.agents.values() if a.is_available])
        healthy = len([a for a in self.agents.values() if a.is_healthy])

        total_tasks = sum(a.total_tasks for a in self.agents.values())
        avg_success_rate = (
            sum(a.success_rate for a in self.agents.values()) / total
            if total > 0 else 0.0
        )

        return {
            "total_agents": total,
            "available_agents": available,
            "healthy_agents": healthy,
            "by_status": by_status,
            "by_tier": by_tier,
            "total_tasks_processed": total_tasks,
            "avg_success_rate": round(avg_success_rate, 2),
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _persist_registry(self) -> None:
        """Save registry to disk."""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "version": "1.0.0",
                "timestamp": datetime.utcnow().isoformat(),
                "agents": {
                    agent_id: manifest.to_dict()
                    for agent_id, manifest in self.agents.items()
                }
            }

            with open(self.registry_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to persist registry: {e}")

    def _load_registry(self) -> None:
        """Load registry from disk."""
        if not self.registry_path.exists():
            return

        try:
            with open(self.registry_path, 'r') as f:
                data = json.load(f)

            for agent_id, agent_data in data.get("agents", {}).items():
                # Reconstruct enums and sets
                agent_data['tier'] = AgentTier(agent_data['tier'])
                agent_data['status'] = AgentStatus(agent_data['status'])
                agent_data['capabilities'] = {
                    AgentCapability(c) for c in agent_data['capabilities']
                }
                agent_data['tags'] = set(agent_data['tags'])

                manifest = AgentManifest(**agent_data)
                self.agents[agent_id] = manifest
        except Exception as e:
            print(f"Warning: Failed to load registry: {e}")


# Global registry instance
_global_registry: Optional[AgentRegistry] = None


def get_registry() -> AgentRegistry:
    """Get global agent registry instance (singleton)."""
    global _global_registry
    if _global_registry is None:
        _global_registry = AgentRegistry()
    return _global_registry
