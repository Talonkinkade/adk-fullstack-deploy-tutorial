"""
Performance Analytics Agent - Agent and system performance monitoring.

This agent scores agents, tracks skill evolution, generates charts,
evaluates bottlenecks, and provides performance insights.
"""

import logging
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from app.agent_platform.core.base_agent import BaseAgent
from app.agent_platform.models.agent import AgentCapability
from app.agent_platform.models.context import ContextType, Insight
from app.agent_platform.models.events import BaseEvent, PerformanceEvent

logger = logging.getLogger(__name__)


class PerformanceAnalyticsAgent(BaseAgent):
    """
    Monitors and analyzes platform and agent performance.

    Capabilities:
    - Track agent performance metrics
    - Detect bottlenecks and anomalies
    - Generate performance reports
    - Score agent effectiveness
    - Trend analysis and predictions
    """

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(
            name="performance_analytics",
            description="Scores agents, tracks skill evolution, generates charts, evaluates bottlenecks",
            version="1.0.0",
            config=config or {},
        )

        self.metrics_buffer: dict[str, list[PerformanceEvent]] = defaultdict(list)
        self.analysis_interval = self.config.get("analysis_interval_seconds", 300)  # 5 min

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    async def setup(self) -> None:
        """Setup the agent."""
        logger.info("Setting up Performance Analytics Agent")

        # Subscribe to performance events
        await self.subscribe("performance.metric", self._handle_performance_metric)
        await self.subscribe("agent.*", self._handle_agent_event)

        # Start periodic analysis
        # TODO: Implement background task for periodic analysis

    async def process_event(self, event: BaseEvent) -> None:
        """Process incoming events."""
        if event.event_type == "performance.metric":
            await self._handle_performance_metric(event)
        elif event.event_type.startswith("agent."):
            await self._handle_agent_event(event)

    # -------------------------------------------------------------------------
    # Capabilities
    # -------------------------------------------------------------------------

    def get_capabilities(self) -> list[AgentCapability]:
        """Declare agent capabilities."""
        return [
            AgentCapability(
                name="track_performance",
                description="Track and store performance metrics",
                input_schema={
                    "type": "object",
                    "properties": {
                        "agent_name": {"type": "string"},
                        "metric_name": {"type": "string"},
                        "metric_value": {"type": "number"},
                    },
                },
            ),
            AgentCapability(
                name="analyze_performance",
                description="Analyze performance data and generate insights",
            ),
            AgentCapability(
                name="detect_bottlenecks",
                description="Identify performance bottlenecks in the system",
            ),
            AgentCapability(
                name="score_agent",
                description="Calculate effectiveness score for an agent",
            ),
        ]

    # -------------------------------------------------------------------------
    # Metric Collection
    # -------------------------------------------------------------------------

    async def _handle_performance_metric(self, event: BaseEvent) -> None:
        """Handle incoming performance metrics."""
        # Convert to PerformanceEvent
        perf_event = PerformanceEvent(
            event_type=event.event_type,
            source_agent=event.source_agent,
            metric_name=event.data.get("metric_name", ""),
            metric_value=event.data.get("metric_value", 0.0),
            metric_unit=event.data.get("metric_unit", ""),
            agent_name=event.data.get("agent_name", event.source_agent),
        )

        # Buffer the event
        self.metrics_buffer[perf_event.agent_name].append(perf_event)

        # Store in context graph
        await self._store_metric(perf_event)

    async def _handle_agent_event(self, event: BaseEvent) -> None:
        """Track agent lifecycle events for performance analysis."""
        if event.event_type == "agent.error":
            # Track error rate
            await self.record_metric(
                agent_name=event.source_agent,
                metric_name="error_count",
                metric_value=1.0,
                metric_unit="errors",
            )

    async def _store_metric(self, metric: PerformanceEvent) -> None:
        """Store metric in context graph."""
        await self.update_context(
            node_type="entity",  # Could create a custom PerformanceMetric type
            properties={
                "agent_name": metric.agent_name,
                "metric_name": metric.metric_name,
                "metric_value": metric.metric_value,
                "metric_unit": metric.metric_unit,
                "timestamp": metric.timestamp.isoformat(),
            },
        )

    async def record_metric(
        self,
        agent_name: str,
        metric_name: str,
        metric_value: float,
        metric_unit: str = "",
    ) -> None:
        """
        Record a performance metric.

        Args:
            agent_name: Name of the agent
            metric_name: Name of the metric
            metric_value: Metric value
            metric_unit: Unit of measurement
        """
        await self.publish_event(
            "performance.metric",
            {
                "agent_name": agent_name,
                "metric_name": metric_name,
                "metric_value": metric_value,
                "metric_unit": metric_unit,
            },
        )

    # -------------------------------------------------------------------------
    # Analysis
    # -------------------------------------------------------------------------

    async def analyze_agent_performance(self, agent_name: str) -> dict[str, Any]:
        """
        Analyze performance for a specific agent.

        Args:
            agent_name: Agent to analyze

        Returns:
            Performance analysis report
        """
        # Query metrics from context graph
        metrics = await self.query_context(
            """
            MATCH (m)
            WHERE m.agent_name = $agent_name
            AND m.timestamp > datetime() - duration({hours: 24})
            RETURN m
            ORDER BY m.timestamp DESC
            """,
            {"agent_name": agent_name},
        )

        if not metrics:
            return {
                "agent_name": agent_name,
                "status": "no_data",
                "message": "No performance data available for the past 24 hours",
            }

        # Calculate statistics
        response_times = []
        error_count = 0
        total_events = 0

        for m_data in metrics:
            m = m_data.get("m", {})
            metric_name = m.get("metric_name", "")

            if metric_name == "response_time_ms":
                response_times.append(m.get("metric_value", 0))
            elif metric_name == "error_count":
                error_count += m.get("metric_value", 0)
            elif metric_name == "events_processed":
                total_events += m.get("metric_value", 0)

        # Calculate performance score (0-100)
        score = await self.calculate_agent_score(agent_name)

        report = {
            "agent_name": agent_name,
            "performance_score": score,
            "metrics": {
                "total_events_processed": total_events,
                "error_count": error_count,
                "error_rate": error_count / total_events if total_events > 0 else 0,
            },
            "analysis_period": "24_hours",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if response_times:
            avg_response = sum(response_times) / len(response_times)
            report["metrics"]["average_response_time_ms"] = avg_response
            report["metrics"]["max_response_time_ms"] = max(response_times)
            report["metrics"]["min_response_time_ms"] = min(response_times)

        # Store as insight
        if self.context_service:
            await self.context_service.store_insight(
                Insight(
                    insight_id=f"perf_analysis_{agent_name}_{datetime.now(timezone.utc).timestamp()}",
                    title=f"Performance Analysis: {agent_name}",
                    description=f"24-hour performance analysis for {agent_name}",
                    insight_type="performance",
                    confidence=0.95,
                    supporting_data=report,
                    affected_nodes=[agent_name],
                    generated_by=self.name,
                    actionable=score < 70,  # Flag if performance is poor
                    actions=(
                        [{"action": "investigate_performance_issues", "reason": "Score below threshold"}]
                        if score < 70
                        else []
                    ),
                )
            )

        return report

    async def calculate_agent_score(self, agent_name: str) -> float:
        """
        Calculate an effectiveness score for an agent (0-100).

        Factors:
        - Error rate (lower is better)
        - Response time (faster is better)
        - Event processing rate (higher is better)
        - Health score

        Args:
            agent_name: Agent to score

        Returns:
            Score from 0 to 100
        """
        # Get agent metadata from registry
        if not self.registry:
            return 50.0  # Default neutral score

        metadata = await self.registry.get_agent(agent_name)

        if not metadata:
            return 0.0

        # Calculate component scores
        health_score = metadata.health_score * 100  # 0-100

        # Error rate score (inverse)
        if metadata.total_events_processed > 0:
            error_rate = metadata.error_count / metadata.total_events_processed
            error_score = max(0, 100 - (error_rate * 1000))  # Penalize errors heavily
        else:
            error_score = 100

        # Response time score (arbitrary threshold of 1000ms)
        if metadata.average_response_time_ms > 0:
            response_score = max(0, 100 - (metadata.average_response_time_ms / 10))
        else:
            response_score = 100

        # Weighted average
        overall_score = (
            health_score * 0.4 + error_score * 0.4 + response_score * 0.2
        )

        return round(overall_score, 2)

    async def detect_bottlenecks(self) -> list[dict[str, Any]]:
        """
        Detect performance bottlenecks across the platform.

        Returns:
            List of detected bottlenecks with recommendations
        """
        bottlenecks = []

        # Check all registered agents
        if not self.registry:
            return bottlenecks

        agents = await self.registry.list_agents()

        for agent in agents:
            # Check response time
            if agent.average_response_time_ms > 500:  # Threshold: 500ms
                bottlenecks.append(
                    {
                        "type": "high_response_time",
                        "agent": agent.name,
                        "value": agent.average_response_time_ms,
                        "threshold": 500,
                        "severity": "medium" if agent.average_response_time_ms < 1000 else "high",
                        "recommendation": "Investigate slow event handlers or database queries",
                    }
                )

            # Check error rate
            if agent.total_events_processed > 0:
                error_rate = agent.error_count / agent.total_events_processed

                if error_rate > 0.05:  # >5% error rate
                    bottlenecks.append(
                        {
                            "type": "high_error_rate",
                            "agent": agent.name,
                            "value": error_rate,
                            "threshold": 0.05,
                            "severity": "high",
                            "recommendation": "Review error logs and add error handling",
                        }
                    )

            # Check health score
            if agent.health_score < 0.7:
                bottlenecks.append(
                    {
                        "type": "low_health_score",
                        "agent": agent.name,
                        "value": agent.health_score,
                        "threshold": 0.7,
                        "severity": "high",
                        "recommendation": "Check agent heartbeat and connectivity",
                    }
                )

        # Generate bottleneck report
        if bottlenecks:
            await self.send_notification(
                f"⚠️ Detected {len(bottlenecks)} performance bottleneck(s). Run analysis for details."
            )

        return bottlenecks

    async def generate_performance_report(self) -> str:
        """
        Generate comprehensive platform performance report.

        Returns:
            Formatted performance report
        """
        if not self.registry:
            return "Registry not available"

        agents = await self.registry.list_agents()

        report_lines = [
            "📊 **Platform Performance Report**\n",
            f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n",
            f"**Total Agents:** {len(agents)}\n\n",
            "**Agent Performance:**\n",
        ]

        for agent in agents:
            score = await self.calculate_agent_score(agent.name)
            status_emoji = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"

            report_lines.append(
                f"{status_emoji} **{agent.name}** - Score: {score}/100\n"
            )
            report_lines.append(f"   - Events Processed: {agent.total_events_processed}\n")
            report_lines.append(f"   - Error Count: {agent.error_count}\n")
            report_lines.append(
                f"   - Avg Response Time: {agent.average_response_time_ms:.2f}ms\n"
            )
            report_lines.append(f"   - Health: {agent.health_score:.2%}\n\n")

        # Detect bottlenecks
        bottlenecks = await self.detect_bottlenecks()

        if bottlenecks:
            report_lines.append("\n**⚠️ Detected Bottlenecks:**\n")

            for bottleneck in bottlenecks:
                report_lines.append(
                    f"- {bottleneck['agent']}: {bottleneck['type']} "
                    f"({bottleneck['severity']} severity)\n"
                )
                report_lines.append(f"  Recommendation: {bottleneck['recommendation']}\n")

        return "".join(report_lines)
