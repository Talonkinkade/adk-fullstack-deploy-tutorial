"""ADA Master Orchestrator - Central control plane for multi-agent system.

Responsibilities:
- Initialize and manage agent lifecycle
- Route requests to appropriate agents
- Monitor system health
- Coordinate tier-2 strategic planning agents
- Manage scaling and resource allocation
"""

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from .config_manager import ADAConfig, get_config
from .health_monitor import HealthMonitor, HealthAlert
from .registry import AgentRegistry, get_registry, AgentManifest, AgentStatus
from .router import RequestRouter, RoutingRequest, RoutingResult, RequestType, RequestPriority


@dataclass
class TaskRequest:
    """High-level task request to ADA orchestrator."""
    task_id: str
    task_type: str
    description: str
    payload: Dict[str, Any]
    priority: RequestPriority = RequestPriority.NORMAL
    user_id: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class TaskResult:
    """Result of task execution."""
    task_id: str
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    agent_id: Optional[str] = None
    execution_time_ms: float = 0.0
    timestamp: float = 0.0


class ADAOrchestrator:
    """Master orchestrator for LearnQwest multi-agent system.

    ADA (Autonomous Development Agent) orchestrates the entire 8-tier agent hierarchy:

    TIER 1: ADA Orchestration (this class)
    TIER 2: Strategic Planning Agents
    TIER 3: Execution Coordinators
    TIER 4: Specialist Workers (60+ agents)
    TIER 5: Data & Analytics
    TIER 6: Intelligence Layer
    TIER 7: Integration Bridges
    TIER 8: Presentation Layer

    Features:
    - Request routing and load balancing
    - Health monitoring and auto-recovery
    - Performance tracking and optimization
    - Integration with existing ADK infrastructure
    """

    def __init__(self, config: Optional[ADAConfig] = None):
        """Initialize ADA orchestrator.

        Args:
            config: Configuration (uses global config if None)
        """
        self.config = config or get_config()
        self.registry = get_registry()
        self.router = RequestRouter(self.registry)
        self.health_monitor = HealthMonitor(
            self.registry,
            check_interval_seconds=self.config.health_check_interval_seconds,
            alert_callback=self._handle_alert
        )

        # Runtime state
        self.is_running = False
        self.start_time: Optional[float] = None

        # Task tracking
        self.active_tasks: Dict[str, TaskRequest] = {}
        self.completed_tasks: int = 0
        self.failed_tasks: int = 0

    async def start(self) -> None:
        """Start the ADA orchestrator."""
        if self.is_running:
            print("ADA orchestrator already running")
            return

        print("=" * 60)
        print("ADA Orchestrator Starting")
        print("=" * 60)

        # Validate configuration
        is_valid, errors = self.config.validate()
        if not is_valid:
            print("Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            raise ValueError("Invalid configuration")

        print(self.config.summary())

        # Start health monitoring
        await self.health_monitor.start()
        print("✓ Health monitor started")

        # Initialize core agents
        await self._initialize_core_agents()

        self.is_running = True
        self.start_time = time.time()

        print("=" * 60)
        print("ADA Orchestrator Ready")
        print(f"Registry: {len(self.registry.agents)} agents registered")
        print("=" * 60)

    async def stop(self) -> None:
        """Stop the ADA orchestrator."""
        if not self.is_running:
            return

        print("Stopping ADA orchestrator...")

        # Stop health monitoring
        await self.health_monitor.stop()
        print("✓ Health monitor stopped")

        self.is_running = False
        print("ADA orchestrator stopped")

    async def execute_task(self, task: TaskRequest) -> TaskResult:
        """Execute a high-level task.

        Args:
            task: Task to execute

        Returns:
            TaskResult with execution outcome
        """
        start_time = time.time()

        if not self.is_running:
            return TaskResult(
                task_id=task.task_id,
                success=False,
                error="ADA orchestrator not running",
                timestamp=time.time()
            )

        # Track active task
        self.active_tasks[task.task_id] = task

        try:
            # Convert task type to request type
            request_type = self._map_task_to_request_type(task.task_type)

            # Create routing request
            routing_request = RoutingRequest(
                request_id=task.task_id,
                request_type=request_type,
                priority=task.priority,
                payload=task.payload,
            )

            # Route to appropriate agent
            routing_result = self.router.route(routing_request)

            if not routing_result.success:
                self.failed_tasks += 1
                return TaskResult(
                    task_id=task.task_id,
                    success=False,
                    error=routing_result.error,
                    execution_time_ms=(time.time() - start_time) * 1000,
                    timestamp=time.time()
                )

            agent = routing_result.agent

            # Mark agent as busy
            agent.increment_load()

            # Execute task on agent
            # TODO: Implement actual agent execution
            # For now, return success
            result = await self._execute_on_agent(agent, task)

            # Update agent metrics
            execution_time_ms = (time.time() - start_time) * 1000
            agent.decrement_load(success=True, response_time_ms=execution_time_ms)

            self.completed_tasks += 1

            return TaskResult(
                task_id=task.task_id,
                success=True,
                result=result,
                agent_id=agent.agent_id,
                execution_time_ms=execution_time_ms,
                timestamp=time.time()
            )

        except Exception as e:
            self.failed_tasks += 1
            return TaskResult(
                task_id=task.task_id,
                success=False,
                error=str(e),
                execution_time_ms=(time.time() - start_time) * 1000,
                timestamp=time.time()
            )
        finally:
            # Remove from active tasks
            self.active_tasks.pop(task.task_id, None)

    async def _execute_on_agent(
        self,
        agent: AgentManifest,
        task: TaskRequest
    ) -> Any:
        """Execute task on specific agent.

        Args:
            agent: Agent to execute on
            task: Task to execute

        Returns:
            Task result
        """
        # TODO: Implement actual agent execution via ADK
        # This would call the ADK API or Agent Engine endpoint
        # For now, simulate execution
        await asyncio.sleep(0.1)  # Simulate work

        return {
            "status": "completed",
            "agent": agent.name,
            "task_id": task.task_id,
            "message": f"Task {task.task_id} executed by {agent.name}"
        }

    def _map_task_to_request_type(self, task_type: str) -> RequestType:
        """Map high-level task type to internal request type."""
        mapping = {
            "goal_planning": RequestType.GOAL_PLANNING,
            "task_decomposition": RequestType.TASK_DECOMPOSITION,
            "code_generation": RequestType.CODE_GENERATION,
            "code_review": RequestType.CODE_REVIEW,
            "testing": RequestType.TESTING,
            "deployment": RequestType.DEPLOYMENT,
            "data_processing": RequestType.DATA_PROCESSING,
            "analytics": RequestType.ANALYTICS,
            "monitoring": RequestType.MONITORING,
            "documentation": RequestType.DOCUMENTATION,
        }
        return mapping.get(task_type, RequestType.GOAL_PLANNING)

    async def _initialize_core_agents(self) -> None:
        """Initialize core tier-1 and tier-2 agents."""
        # This would register the existing ADK goal planning agent
        # and any other core agents that should always be available
        print("Initializing core agents...")

        # TODO: Register existing ADK goal planning agent
        # TODO: Initialize tier-2 strategic planning agents
        # TODO: Initialize tier-3 coordinators

        print("✓ Core agents initialized")

    def _handle_alert(self, alert: HealthAlert) -> None:
        """Handle health alerts from monitoring system.

        Args:
            alert: Health alert
        """
        # TODO: Implement alert handling logic
        # - Send notifications
        # - Trigger auto-recovery
        # - Log to monitoring system
        pass

    def get_status(self) -> dict:
        """Get current orchestrator status."""
        uptime = time.time() - self.start_time if self.start_time else 0

        return {
            "status": "running" if self.is_running else "stopped",
            "uptime_seconds": uptime,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat() if self.start_time else None,
            "active_tasks": len(self.active_tasks),
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "success_rate": (
                (self.completed_tasks / (self.completed_tasks + self.failed_tasks) * 100)
                if (self.completed_tasks + self.failed_tasks) > 0
                else 0.0
            ),
            "agents": self.registry.get_statistics(),
            "health": self.health_monitor.get_system_health(),
            "routing": self.router.get_routing_statistics(),
        }

    def get_metrics(self) -> dict:
        """Get detailed performance metrics."""
        return {
            "orchestrator": self.get_status(),
            "agents": {
                agent_id: {
                    "name": agent.name,
                    "tier": agent.tier.value,
                    "status": agent.status.value,
                    "load": agent.current_load,
                    "total_tasks": agent.total_tasks,
                    "success_rate": round(agent.success_rate, 2),
                    "avg_response_time_ms": round(agent.avg_response_time_ms, 2),
                }
                for agent_id, agent in self.registry.agents.items()
            }
        }


# Global orchestrator instance
_global_orchestrator: Optional[ADAOrchestrator] = None


async def get_orchestrator() -> ADAOrchestrator:
    """Get global orchestrator instance (singleton)."""
    global _global_orchestrator
    if _global_orchestrator is None:
        _global_orchestrator = ADAOrchestrator()
        await _global_orchestrator.start()
    return _global_orchestrator


async def shutdown_orchestrator() -> None:
    """Shutdown global orchestrator."""
    global _global_orchestrator
    if _global_orchestrator:
        await _global_orchestrator.stop()
        _global_orchestrator = None
