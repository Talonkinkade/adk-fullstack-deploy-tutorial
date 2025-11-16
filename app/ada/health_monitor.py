"""Health Monitor - Real-time agent health monitoring and auto-recovery.

Monitors:
- Agent heartbeats
- Task completion rates
- Error rates and anomalies
- Resource utilization

Triggers:
- Auto-recovery for failed agents
- Alerting for degraded performance
- Scaling decisions
"""

import asyncio
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Deque, Dict, List, Optional, Callable

from .registry import AgentRegistry, AgentStatus, AgentManifest


@dataclass
class HealthMetrics:
    """Health metrics for an agent."""
    agent_id: str
    timestamp: float = field(default_factory=time.time)

    # Heartbeat
    last_heartbeat: float = 0.0
    heartbeat_interval_seconds: float = 30.0

    # Performance
    success_rate: float = 100.0
    avg_response_time_ms: float = 0.0
    current_load: int = 0

    # Errors
    consecutive_failures: int = 0
    error_rate: float = 0.0

    # Status
    is_healthy: bool = True
    is_available: bool = True

    @property
    def time_since_heartbeat(self) -> float:
        """Seconds since last heartbeat."""
        return time.time() - self.last_heartbeat

    @property
    def is_unresponsive(self) -> bool:
        """Check if agent hasn't sent heartbeat in expected interval."""
        return self.time_since_heartbeat > (self.heartbeat_interval_seconds * 2)


@dataclass
class HealthAlert:
    """Health alert for degraded agent."""
    agent_id: str
    severity: str  # "warning", "error", "critical"
    message: str
    timestamp: float = field(default_factory=time.time)
    metrics: Optional[HealthMetrics] = None


class HealthMonitor:
    """Monitor agent health and trigger recovery actions.

    Features:
    - Continuous heartbeat monitoring
    - Performance degradation detection
    - Automatic recovery for failed agents
    - Alert generation
    """

    def __init__(
        self,
        registry: AgentRegistry,
        check_interval_seconds: int = 30,
        alert_callback: Optional[Callable[[HealthAlert], None]] = None
    ):
        """Initialize health monitor.

        Args:
            registry: Agent registry to monitor
            check_interval_seconds: How often to run health checks
            alert_callback: Optional callback for alerts
        """
        self.registry = registry
        self.check_interval = check_interval_seconds
        self.alert_callback = alert_callback

        # Metrics storage (agent_id -> deque of metrics)
        self.metrics_history: Dict[str, Deque[HealthMetrics]] = defaultdict(
            lambda: deque(maxlen=100)  # Keep last 100 metrics per agent
        )

        # Alerts
        self.alerts: Deque[HealthAlert] = deque(maxlen=1000)

        # Monitoring state
        self.is_running = False
        self._monitor_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start health monitoring loop."""
        if self.is_running:
            return

        self.is_running = True
        self._monitor_task = asyncio.create_task(self._monitor_loop())

    async def stop(self) -> None:
        """Stop health monitoring loop."""
        self.is_running = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass

    async def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self.is_running:
            try:
                await self._run_health_checks()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                print(f"Error in health monitor loop: {e}")
                await asyncio.sleep(self.check_interval)

    async def _run_health_checks(self) -> None:
        """Run health checks on all registered agents."""
        for agent_id, agent in self.registry.agents.items():
            metrics = self._collect_metrics(agent)
            self.metrics_history[agent_id].append(metrics)

            # Check for issues
            if not metrics.is_healthy:
                await self._handle_unhealthy_agent(agent, metrics)
            elif metrics.is_unresponsive:
                await self._handle_unresponsive_agent(agent, metrics)
            elif metrics.error_rate > 50.0:
                await self._handle_high_error_rate(agent, metrics)

    def _collect_metrics(self, agent: AgentManifest) -> HealthMetrics:
        """Collect current metrics for an agent."""
        return HealthMetrics(
            agent_id=agent.agent_id,
            last_heartbeat=agent.last_heartbeat,
            success_rate=agent.success_rate,
            avg_response_time_ms=agent.avg_response_time_ms,
            current_load=agent.current_load,
            consecutive_failures=self._get_consecutive_failures(agent.agent_id),
            error_rate=100.0 - agent.success_rate,
            is_healthy=agent.is_healthy,
            is_available=agent.is_available,
        )

    def _get_consecutive_failures(self, agent_id: str) -> int:
        """Get count of consecutive failures from recent history."""
        history = self.metrics_history.get(agent_id, deque())
        if not history:
            return 0

        consecutive = 0
        for metrics in reversed(history):
            if metrics.error_rate > 0:
                consecutive += 1
            else:
                break

        return consecutive

    async def _handle_unhealthy_agent(
        self,
        agent: AgentManifest,
        metrics: HealthMetrics
    ) -> None:
        """Handle unhealthy agent - trigger recovery."""
        alert = HealthAlert(
            agent_id=agent.agent_id,
            severity="error",
            message=f"Agent {agent.name} is unhealthy",
            metrics=metrics,
        )
        await self._emit_alert(alert)

        # Mark as offline
        self.registry.update_status(agent.agent_id, AgentStatus.OFFLINE)

        # TODO: Trigger recovery (restart, replace, etc.)

    async def _handle_unresponsive_agent(
        self,
        agent: AgentManifest,
        metrics: HealthMetrics
    ) -> None:
        """Handle unresponsive agent (no heartbeat)."""
        alert = HealthAlert(
            agent_id=agent.agent_id,
            severity="critical",
            message=f"Agent {agent.name} unresponsive for {metrics.time_since_heartbeat:.0f}s",
            metrics=metrics,
        )
        await self._emit_alert(alert)

        # Mark as error state
        self.registry.update_status(agent.agent_id, AgentStatus.ERROR)

    async def _handle_high_error_rate(
        self,
        agent: AgentManifest,
        metrics: HealthMetrics
    ) -> None:
        """Handle agent with high error rate."""
        alert = HealthAlert(
            agent_id=agent.agent_id,
            severity="warning",
            message=f"Agent {agent.name} has high error rate: {metrics.error_rate:.1f}%",
            metrics=metrics,
        )
        await self._emit_alert(alert)

    async def _emit_alert(self, alert: HealthAlert) -> None:
        """Emit a health alert."""
        self.alerts.append(alert)
        print(f"[{alert.severity.upper()}] {alert.message}")

        if self.alert_callback:
            try:
                if asyncio.iscoroutinefunction(self.alert_callback):
                    await self.alert_callback(alert)
                else:
                    self.alert_callback(alert)
            except Exception as e:
                print(f"Error in alert callback: {e}")

    def get_agent_health(self, agent_id: str) -> Optional[HealthMetrics]:
        """Get latest health metrics for an agent."""
        history = self.metrics_history.get(agent_id)
        if not history:
            return None
        return history[-1]

    def get_recent_alerts(self, limit: int = 10) -> List[HealthAlert]:
        """Get recent alerts."""
        return list(self.alerts)[-limit:]

    def get_system_health(self) -> dict:
        """Get overall system health summary."""
        total_agents = len(self.registry.agents)
        if total_agents == 0:
            return {
                "status": "no_agents",
                "total_agents": 0,
                "healthy_agents": 0,
                "unhealthy_agents": 0,
                "unresponsive_agents": 0,
                "timestamp": datetime.utcnow().isoformat(),
            }

        healthy = 0
        unhealthy = 0
        unresponsive = 0

        for agent_id in self.registry.agents:
            metrics = self.get_agent_health(agent_id)
            if not metrics:
                continue

            if metrics.is_unresponsive:
                unresponsive += 1
            elif metrics.is_healthy:
                healthy += 1
            else:
                unhealthy += 1

        # Determine overall status
        health_percentage = (healthy / total_agents) * 100
        if health_percentage >= 90:
            status = "healthy"
        elif health_percentage >= 70:
            status = "degraded"
        else:
            status = "critical"

        return {
            "status": status,
            "health_percentage": round(health_percentage, 1),
            "total_agents": total_agents,
            "healthy_agents": healthy,
            "unhealthy_agents": unhealthy,
            "unresponsive_agents": unresponsive,
            "recent_alerts": len([a for a in self.alerts if time.time() - a.timestamp < 300]),  # last 5 min
            "timestamp": datetime.utcnow().isoformat(),
        }
