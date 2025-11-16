"""Agent Performance Scorer - Calculate composite performance scores.

Scoring components:
1. Performance (40%): Success rate + response time
2. Reliability (30%): Uptime + consistency
3. Efficiency (20%): Resource usage optimization
4. Collaboration (10%): Team interactions
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from ..schemas.metrics_schema import AgentMetrics
from ..schemas.leaderboard_schema import AgentScore, ACHIEVEMENT_BADGES
from ..ada.registry import AgentRegistry, AgentManifest


class AgentScorer:
    """Calculate and manage agent performance scores.

    Features:
    - Multi-dimensional scoring
    - Weighted composite scores
    - Badge/achievement tracking
    - Trend detection
    """

    # Scoring weights (sum to 1.0)
    DEFAULT_WEIGHTS = {
        "performance": 0.40,
        "reliability": 0.30,
        "efficiency": 0.20,
        "collaboration": 0.10,
    }

    def __init__(
        self,
        registry: AgentRegistry,
        weights: Optional[Dict[str, float]] = None
    ):
        """Initialize scorer.

        Args:
            registry: Agent registry for data
            weights: Custom scoring weights
        """
        self.registry = registry
        self.weights = weights or self.DEFAULT_WEIGHTS

        # Validate weights sum to 1.0
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total}")

    def calculate_score(self, agent: AgentManifest) -> AgentScore:
        """Calculate composite score for an agent.

        Args:
            agent: Agent to score

        Returns:
            AgentScore with all components
        """
        score = AgentScore(
            agent_id=agent.agent_id,
            agent_name=agent.name,
            tier=agent.tier.value,
            weights=self.weights
        )

        # Calculate component scores
        score.performance_score = self._calculate_performance_score(agent)
        score.reliability_score = self._calculate_reliability_score(agent)
        score.efficiency_score = self._calculate_efficiency_score(agent)
        score.collaboration_score = self._calculate_collaboration_score(agent)

        # Calculate weighted total
        score.calculate_total_score()

        return score

    def _calculate_performance_score(self, agent: AgentManifest) -> float:
        """Calculate performance score (0-100).

        Components:
        - Success rate (70%)
        - Response time (30%)
        """
        if agent.total_tasks == 0:
            return 0.0

        # Success rate component (0-100)
        success_component = agent.success_rate * 0.70

        # Response time component (inverted - lower is better)
        # Normalize to 0-100 scale (assume 5000ms = 0, 100ms = 100)
        max_response_time = 5000.0
        min_response_time = 100.0

        if agent.avg_response_time_ms <= min_response_time:
            response_component = 100.0
        elif agent.avg_response_time_ms >= max_response_time:
            response_component = 0.0
        else:
            # Linear interpolation
            response_component = (
                (max_response_time - agent.avg_response_time_ms) /
                (max_response_time - min_response_time)
            ) * 100.0

        response_component *= 0.30

        return success_component + response_component

    def _calculate_reliability_score(self, agent: AgentManifest) -> float:
        """Calculate reliability score (0-100).

        Components:
        - Heartbeat health (50%)
        - Consistency of performance (50%)
        """
        # Heartbeat health
        if agent.is_healthy:
            heartbeat_component = 100.0 * 0.50
        else:
            # Degrade based on time since last heartbeat
            time_since_heartbeat = datetime.now().timestamp() - agent.last_heartbeat
            max_acceptable_gap = 300  # 5 minutes
            heartbeat_component = max(
                0,
                (1.0 - min(time_since_heartbeat / max_acceptable_gap, 1.0)) * 100.0 * 0.50
            )

        # Consistency (simple version - based on success rate)
        consistency_component = agent.success_rate * 0.50

        return heartbeat_component + consistency_component

    def _calculate_efficiency_score(self, agent: AgentManifest) -> float:
        """Calculate efficiency score (0-100).

        Components:
        - Response time (faster = more efficient)
        - Load handling (capacity utilization)
        """
        if agent.total_tasks == 0:
            return 50.0  # Neutral score for new agents

        # Response time efficiency (same as in performance)
        max_response_time = 5000.0
        min_response_time = 100.0

        if agent.avg_response_time_ms <= min_response_time:
            time_efficiency = 100.0
        elif agent.avg_response_time_ms >= max_response_time:
            time_efficiency = 0.0
        else:
            time_efficiency = (
                (max_response_time - agent.avg_response_time_ms) /
                (max_response_time - min_response_time)
            ) * 100.0

        # Load handling (prefer agents that can handle their max load)
        if agent.max_concurrent_tasks > 0:
            # Agents with higher capacity are valued
            load_score = min(agent.max_concurrent_tasks * 20, 100.0)
        else:
            load_score = 0.0

        return (time_efficiency * 0.70) + (load_score * 0.30)

    def _calculate_collaboration_score(self, agent: AgentManifest) -> float:
        """Calculate collaboration score (0-100).

        This is a placeholder - would need collaboration tracking data.
        For now, returns a baseline score.
        """
        # TODO: Integrate with Neo4j collaboration data
        # For now, return neutral score
        return 50.0

    def calculate_leaderboard(
        self,
        tier: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[AgentScore]:
        """Calculate scores for all agents and return sorted leaderboard.

        Args:
            tier: Filter by tier (optional)
            limit: Limit results (optional)

        Returns:
            Sorted list of agent scores (best first)
        """
        agents = list(self.registry.agents.values())

        # Filter by tier if specified
        if tier is not None:
            agents = [a for a in agents if a.tier.value == tier]

        # Calculate scores
        scores = [self.calculate_score(agent) for agent in agents]

        # Sort by total score (descending)
        scores.sort(key=lambda s: s.total_score, reverse=True)

        # Limit results if specified
        if limit is not None:
            scores = scores[:limit]

        return scores

    def award_badges(
        self,
        agent: AgentManifest,
        historical_data: Optional[Dict] = None
    ) -> List[str]:
        """Determine which badges an agent should receive.

        Args:
            agent: Agent to evaluate
            historical_data: Historical performance data (optional)

        Returns:
            List of badge IDs awarded
        """
        badges = []

        # Perfect Week badge
        if historical_data and historical_data.get("consecutive_days_100_success", 0) >= 7:
            badges.append("perfect_week")

        # Workhorse badge (most tasks)
        if agent.total_tasks >= 1000:
            badges.append("workhorse")

        # Reliable badge (99%+ success rate with significant volume)
        if agent.success_rate >= 99.0 and agent.total_tasks >= 100:
            badges.append("reliable")

        # TODO: Add more badge logic with historical data

        return badges

    def get_percentile_rank(
        self,
        agent_id: str,
        tier: Optional[int] = None
    ) -> Optional[float]:
        """Get agent's percentile rank (0-100).

        Args:
            agent_id: Agent to rank
            tier: Compare within tier only (optional)

        Returns:
            Percentile rank (100 = best, 0 = worst) or None if not found
        """
        leaderboard = self.calculate_leaderboard(tier=tier)

        # Find agent in leaderboard
        for i, score in enumerate(leaderboard):
            if score.agent_id == agent_id:
                # Calculate percentile
                percentile = ((len(leaderboard) - i) / len(leaderboard)) * 100
                return percentile

        return None

    def get_performance_summary(self, agent_id: str) -> Dict:
        """Get comprehensive performance summary for an agent.

        Args:
            agent_id: Agent to summarize

        Returns:
            Dictionary with performance summary
        """
        agent = self.registry.get(agent_id)
        if not agent:
            return {"error": "Agent not found"}

        score = self.calculate_score(agent)
        percentile = self.get_percentile_rank(agent_id)
        tier_percentile = self.get_percentile_rank(agent_id, tier=agent.tier.value)

        return {
            "agent_id": agent_id,
            "agent_name": agent.name,
            "tier": agent.tier.value,
            "score": score.to_dict(),
            "percentile_rank": round(percentile, 1) if percentile else None,
            "tier_percentile_rank": round(tier_percentile, 1) if tier_percentile else None,
            "total_tasks": agent.total_tasks,
            "success_rate": round(agent.success_rate, 2),
            "avg_response_time_ms": round(agent.avg_response_time_ms, 2),
            "is_healthy": agent.is_healthy,
            "is_available": agent.is_available,
        }
