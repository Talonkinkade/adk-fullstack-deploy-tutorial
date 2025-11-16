"""Leaderboard schemas and scoring models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class AgentScore:
    """Composite agent score for leaderboard."""
    agent_id: str
    agent_name: str
    tier: int

    # Score components (0-100 each)
    performance_score: float = 0.0  # Success rate + response time
    reliability_score: float = 0.0  # Uptime + consistency
    efficiency_score: float = 0.0   # Resource usage
    collaboration_score: float = 0.0  # Team interactions

    # Composite score (weighted average)
    total_score: float = 0.0

    # Weights for composite score
    weights: Dict[str, float] = field(default_factory=lambda: {
        "performance": 0.40,
        "reliability": 0.30,
        "efficiency": 0.20,
        "collaboration": 0.10,
    })

    def calculate_total_score(self) -> float:
        """Calculate weighted total score."""
        self.total_score = (
            self.performance_score * self.weights["performance"] +
            self.reliability_score * self.weights["reliability"] +
            self.efficiency_score * self.weights["efficiency"] +
            self.collaboration_score * self.weights["collaboration"]
        )
        return self.total_score

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "tier": self.tier,
            "performance_score": round(self.performance_score, 2),
            "reliability_score": round(self.reliability_score, 2),
            "efficiency_score": round(self.efficiency_score, 2),
            "collaboration_score": round(self.collaboration_score, 2),
            "total_score": round(self.total_score, 2),
            "weights": self.weights,
        }


@dataclass
class LeaderboardEntry:
    """Single leaderboard entry with ranking."""
    rank: int
    agent_score: AgentScore
    previous_rank: Optional[int] = None
    rank_change: Optional[int] = None

    # Achievements/badges
    badges: List[str] = field(default_factory=list)

    # Period info
    period: str = "all_time"  # "daily", "weekly", "monthly", "all_time"
    calculated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_improving(self) -> bool:
        """Check if rank improved."""
        if self.previous_rank is None or self.rank_change is None:
            return False
        return self.rank_change > 0

    @property
    def is_declining(self) -> bool:
        """Check if rank declined."""
        if self.previous_rank is None or self.rank_change is None:
            return False
        return self.rank_change < 0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank,
            "agent": self.agent_score.to_dict(),
            "previous_rank": self.previous_rank,
            "rank_change": self.rank_change,
            "is_improving": self.is_improving,
            "is_declining": self.is_declining,
            "badges": self.badges,
            "period": self.period,
            "calculated_at": self.calculated_at.isoformat(),
        }


# Achievement badge definitions
ACHIEVEMENT_BADGES = {
    "perfect_week": {
        "name": "Perfect Week",
        "description": "100% success rate for 7 consecutive days",
        "icon": "🏆",
    },
    "speed_demon": {
        "name": "Speed Demon",
        "description": "Fastest average response time in tier",
        "icon": "⚡",
    },
    "workhorse": {
        "name": "Workhorse",
        "description": "Most tasks completed in period",
        "icon": "💪",
    },
    "team_player": {
        "name": "Team Player",
        "description": "Most agent collaborations",
        "icon": "🤝",
    },
    "reliable": {
        "name": "Rock Solid",
        "description": "99%+ uptime for 30 days",
        "icon": "🗿",
    },
    "rising_star": {
        "name": "Rising Star",
        "description": "Biggest rank improvement this week",
        "icon": "🌟",
    },
    "efficiency_expert": {
        "name": "Efficiency Expert",
        "description": "Lowest resource usage per task",
        "icon": "🎯",
    },
}
