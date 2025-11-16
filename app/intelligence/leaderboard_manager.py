"""Leaderboard Manager - Manage gamified agent rankings and achievements."""

from datetime import datetime
from typing import Dict, List, Optional

from ..ada.registry import AgentRegistry
from ..schemas.leaderboard_schema import LeaderboardEntry, AgentScore, ACHIEVEMENT_BADGES
from .scorer import AgentScorer


class LeaderboardManager:
    """Manage leaderboards and achievement tracking.

    Features:
    - Multiple leaderboard periods (daily, weekly, monthly, all-time)
    - Rank change tracking
    - Badge/achievement awarding
    - Historical rankings
    """

    def __init__(
        self,
        registry: AgentRegistry,
        scorer: Optional[AgentScorer] = None
    ):
        """Initialize leaderboard manager.

        Args:
            registry: Agent registry
            scorer: Agent scorer (creates one if not provided)
        """
        self.registry = registry
        self.scorer = scorer or AgentScorer(registry)

        # Store previous rankings for change tracking
        self.previous_rankings: Dict[str, Dict[str, int]] = {
            "daily": {},
            "weekly": {},
            "monthly": {},
            "all_time": {},
        }

    def generate_leaderboard(
        self,
        period: str = "all_time",
        tier: Optional[int] = None,
        limit: int = 100
    ) -> List[LeaderboardEntry]:
        """Generate leaderboard for a period.

        Args:
            period: Period type ("daily", "weekly", "monthly", "all_time")
            tier: Filter by tier (optional)
            limit: Maximum entries to return

        Returns:
            List of leaderboard entries with rankings
        """
        # Calculate scores for all agents
        scores = self.scorer.calculate_leaderboard(tier=tier, limit=limit)

        # Create leaderboard entries
        entries = []
        for rank, score in enumerate(scores, start=1):
            # Get previous rank for this agent
            prev_rank = self.previous_rankings[period].get(score.agent_id)

            # Calculate rank change
            rank_change = None
            if prev_rank is not None:
                rank_change = prev_rank - rank  # Positive = improved

            # Award badges
            agent = self.registry.get(score.agent_id)
            badges = self.scorer.award_badges(agent) if agent else []

            # Create entry
            entry = LeaderboardEntry(
                rank=rank,
                agent_score=score,
                previous_rank=prev_rank,
                rank_change=rank_change,
                badges=badges,
                period=period,
                calculated_at=datetime.utcnow()
            )

            entries.append(entry)

        # Update previous rankings
        self.previous_rankings[period] = {
            entry.agent_score.agent_id: entry.rank
            for entry in entries
        }

        return entries

    def get_agent_rank(
        self,
        agent_id: str,
        period: str = "all_time",
        tier: Optional[int] = None
    ) -> Optional[LeaderboardEntry]:
        """Get leaderboard entry for a specific agent.

        Args:
            agent_id: Agent to find
            period: Period type
            tier: Filter by tier (optional)

        Returns:
            LeaderboardEntry or None if not found
        """
        leaderboard = self.generate_leaderboard(period=period, tier=tier, limit=1000)

        for entry in leaderboard:
            if entry.agent_score.agent_id == agent_id:
                return entry

        return None

    def get_top_performers(
        self,
        period: str = "all_time",
        limit: int = 10
    ) -> List[LeaderboardEntry]:
        """Get top performers for a period.

        Args:
            period: Period type
            limit: Number of top performers

        Returns:
            List of top leaderboard entries
        """
        return self.generate_leaderboard(period=period, limit=limit)

    def get_tier_leaders(self, period: str = "all_time") -> Dict[int, LeaderboardEntry]:
        """Get the leader from each tier.

        Args:
            period: Period type

        Returns:
            Dictionary mapping tier -> leader entry
        """
        leaders = {}

        for tier in range(1, 9):  # Tiers 1-8
            tier_leaderboard = self.generate_leaderboard(
                period=period,
                tier=tier,
                limit=1
            )

            if tier_leaderboard:
                leaders[tier] = tier_leaderboard[0]

        return leaders

    def get_achievements_summary(self) -> Dict[str, int]:
        """Get summary of all achievements awarded.

        Returns:
            Dictionary mapping badge ID -> count of agents with that badge
        """
        badge_counts = {badge_id: 0 for badge_id in ACHIEVEMENT_BADGES.keys()}

        # Generate current leaderboard
        leaderboard = self.generate_leaderboard(limit=1000)

        # Count badges
        for entry in leaderboard:
            for badge in entry.badges:
                if badge in badge_counts:
                    badge_counts[badge] += 1

        return badge_counts

    def get_rising_stars(
        self,
        period: str = "weekly",
        limit: int = 10
    ) -> List[LeaderboardEntry]:
        """Get agents with biggest rank improvements.

        Args:
            period: Period to check
            limit: Number of rising stars

        Returns:
            List of leaderboard entries sorted by rank improvement
        """
        leaderboard = self.generate_leaderboard(period=period, limit=1000)

        # Filter to agents with rank changes
        improving = [
            entry for entry in leaderboard
            if entry.rank_change is not None and entry.rank_change > 0
        ]

        # Sort by rank improvement (descending)
        improving.sort(key=lambda e: e.rank_change, reverse=True)

        return improving[:limit]

    def get_leaderboard_summary(self, period: str = "all_time") -> Dict:
        """Get summary statistics for a leaderboard.

        Args:
            period: Period type

        Returns:
            Summary dictionary
        """
        leaderboard = self.generate_leaderboard(period=period, limit=1000)

        if not leaderboard:
            return {
                "period": period,
                "total_agents": 0,
                "avg_score": 0.0,
                "top_score": 0.0,
                "bottom_score": 0.0,
            }

        scores = [entry.agent_score.total_score for entry in leaderboard]
        avg_score = sum(scores) / len(scores)

        return {
            "period": period,
            "total_agents": len(leaderboard),
            "avg_score": round(avg_score, 2),
            "top_score": round(scores[0], 2),
            "bottom_score": round(scores[-1], 2),
            "agents_improving": len([e for e in leaderboard if e.is_improving]),
            "agents_declining": len([e for e in leaderboard if e.is_declining]),
            "calculated_at": datetime.utcnow().isoformat(),
        }

    def export_leaderboard(
        self,
        period: str = "all_time",
        format: str = "json"
    ) -> str:
        """Export leaderboard in various formats.

        Args:
            period: Period type
            format: Export format ("json", "markdown", "csv")

        Returns:
            Formatted leaderboard string
        """
        leaderboard = self.generate_leaderboard(period=period, limit=1000)

        if format == "json":
            import json
            return json.dumps(
                [entry.to_dict() for entry in leaderboard],
                indent=2
            )

        elif format == "markdown":
            lines = [f"# Leaderboard - {period.replace('_', ' ').title()}\n"]
            lines.append("| Rank | Agent | Tier | Score | Change | Badges |")
            lines.append("|------|-------|------|-------|--------|--------|")

            for entry in leaderboard:
                rank_change_str = (
                    f"+{entry.rank_change}" if entry.rank_change and entry.rank_change > 0
                    else str(entry.rank_change) if entry.rank_change
                    else "-"
                )
                badges_str = " ".join(entry.badges[:3])  # Show max 3 badges

                lines.append(
                    f"| {entry.rank} | {entry.agent_score.agent_name} | "
                    f"{entry.agent_score.tier} | {entry.agent_score.total_score:.1f} | "
                    f"{rank_change_str} | {badges_str} |"
                )

            return "\n".join(lines)

        elif format == "csv":
            lines = ["Rank,Agent,Tier,Score,Previous Rank,Rank Change,Badges"]

            for entry in leaderboard:
                badges_str = ";".join(entry.badges)
                lines.append(
                    f"{entry.rank},{entry.agent_score.agent_name},"
                    f"{entry.agent_score.tier},{entry.agent_score.total_score:.2f},"
                    f"{entry.previous_rank or ''},"
                    f"{entry.rank_change or ''},"
                    f"\"{badges_str}\""
                )

            return "\n".join(lines)

        else:
            raise ValueError(f"Unsupported format: {format}")
