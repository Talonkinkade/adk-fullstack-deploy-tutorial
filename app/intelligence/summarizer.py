"""Auto-Summary Generator - Generate natural language summaries of agent performance.

Generates:
- Daily activity summaries
- Weekly performance reports
- Monthly trend analyses
- Custom period summaries
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict

from google import genai
from google.genai import types

from ..ada.registry import AgentRegistry
from ..schemas.leaderboard_schema import LeaderboardEntry


class AutoSummarizer:
    """Generate natural language summaries using LLM.

    Features:
    - Daily/weekly/monthly summaries
    - Trend analysis
    - Performance highlights
    - Recommendations
    """

    SUMMARY_PROMPT_TEMPLATE = """You are an AI assistant that generates concise performance summaries for agent systems.

Given the following performance data, generate a clear, professional summary in markdown format.

**Data:**
{data}

**Instructions:**
1. Start with an executive summary (2-3 sentences)
2. Highlight top performers
3. Note any concerning trends
4. Provide 2-3 actionable recommendations
5. Keep it under 300 words
6. Use bullet points and sections

Generate the summary now:
"""

    def __init__(self, registry: AgentRegistry, model: str = "gemini-2.5-flash"):
        """Initialize summarizer.

        Args:
            registry: Agent registry
            model: LLM model to use
        """
        self.registry = registry
        self.model_name = model
        self.client = genai.Client()

    def generate_daily_summary(
        self,
        date: Optional[datetime] = None
    ) -> str:
        """Generate daily performance summary.

        Args:
            date: Date to summarize (defaults to today)

        Returns:
            Markdown summary
        """
        if date is None:
            date = datetime.now()

        # Gather data
        stats = self.registry.get_statistics()

        data = {
            "date": date.strftime("%Y-%m-%d"),
            "period": "Daily",
            "total_agents": stats["total_agents"],
            "available_agents": stats["available_agents"],
            "total_tasks_processed": stats["total_tasks_processed"],
            "avg_success_rate": stats["avg_success_rate"],
        }

        return self._generate_summary(data, "daily")

    def generate_weekly_summary(
        self,
        week_start: Optional[datetime] = None
    ) -> str:
        """Generate weekly performance summary.

        Args:
            week_start: Start of week (defaults to current week)

        Returns:
            Markdown summary
        """
        if week_start is None:
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())

        stats = self.registry.get_statistics()

        data = {
            "week_start": week_start.strftime("%Y-%m-%d"),
            "period": "Weekly",
            "total_agents": stats["total_agents"],
            "available_agents": stats["available_agents"],
            "total_tasks_processed": stats["total_tasks_processed"],
            "avg_success_rate": stats["avg_success_rate"],
        }

        return self._generate_summary(data, "weekly")

    def generate_agent_summary(
        self,
        agent_id: str,
        period_days: int = 7
    ) -> str:
        """Generate summary for a specific agent.

        Args:
            agent_id: Agent to summarize
            period_days: Number of days to analyze

        Returns:
            Markdown summary
        """
        agent = self.registry.get(agent_id)
        if not agent:
            return f"Agent {agent_id} not found."

        data = {
            "agent_name": agent.name,
            "agent_id": agent_id,
            "tier": agent.tier.value,
            "period_days": period_days,
            "total_tasks": agent.total_tasks,
            "success_rate": round(agent.success_rate, 2),
            "avg_response_time_ms": round(agent.avg_response_time_ms, 2),
            "current_status": agent.status.value,
        }

        return self._generate_summary(data, "agent")

    def generate_leaderboard_summary(
        self,
        leaderboard: List[LeaderboardEntry],
        period: str = "weekly"
    ) -> str:
        """Generate summary of leaderboard results.

        Args:
            leaderboard: Leaderboard entries
            period: Period type

        Returns:
            Markdown summary
        """
        if not leaderboard:
            return "No leaderboard data available."

        # Get top 5
        top_performers = leaderboard[:5]

        data = {
            "period": period,
            "total_agents": len(leaderboard),
            "top_performers": [
                {
                    "rank": entry.rank,
                    "name": entry.agent_score.agent_name,
                    "score": round(entry.agent_score.total_score, 2),
                    "badges": entry.badges,
                }
                for entry in top_performers
            ],
        }

        return self._generate_summary(data, "leaderboard")

    def _generate_summary(
        self,
        data: Dict,
        summary_type: str
    ) -> str:
        """Generate summary using LLM.

        Args:
            data: Data to summarize
            summary_type: Type of summary

        Returns:
            Generated summary
        """
        # Format data as readable text
        data_text = self._format_data(data)

        prompt = self.SUMMARY_PROMPT_TEMPLATE.format(data=data_text)

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=1024,
                )
            )

            return response.text.strip()

        except Exception as e:
            print(f"Error generating summary: {e}")
            # Fallback to template-based summary
            return self._generate_template_summary(data, summary_type)

    def _format_data(self, data: Dict) -> str:
        """Format data dictionary as readable text."""
        lines = []
        for key, value in data.items():
            # Convert snake_case to Title Case
            key_formatted = key.replace("_", " ").title()
            lines.append(f"- {key_formatted}: {value}")
        return "\n".join(lines)

    def _generate_template_summary(
        self,
        data: Dict,
        summary_type: str
    ) -> str:
        """Generate simple template-based summary (fallback).

        Args:
            data: Data to summarize
            summary_type: Type of summary

        Returns:
            Template-based summary
        """
        if summary_type == "daily":
            return f"""# Daily Performance Summary - {data.get('date', 'N/A')}

## Overview
- **Total Agents:** {data.get('total_agents', 0)}
- **Available Agents:** {data.get('available_agents', 0)}
- **Tasks Processed:** {data.get('total_tasks_processed', 0)}
- **Average Success Rate:** {data.get('avg_success_rate', 0):.2f}%

## Status
System operating normally.
"""

        elif summary_type == "agent":
            return f"""# Agent Summary - {data.get('agent_name', 'Unknown')}

## Performance Metrics
- **Agent ID:** {data.get('agent_id', 'N/A')}
- **Tier:** {data.get('tier', 'N/A')}
- **Total Tasks:** {data.get('total_tasks', 0)}
- **Success Rate:** {data.get('success_rate', 0):.2f}%
- **Avg Response Time:** {data.get('avg_response_time_ms', 0):.2f}ms
- **Status:** {data.get('current_status', 'unknown')}

## Analysis
Agent is performing as expected.
"""

        elif summary_type == "leaderboard":
            top_performers_text = "\n".join([
                f"{i+1}. **{p['name']}** - Score: {p['score']} {' '.join(p.get('badges', []))}"
                for i, p in enumerate(data.get('top_performers', []))
            ])

            return f"""# Leaderboard Summary - {data.get('period', 'N/A').title()}

## Top Performers
{top_performers_text}

## Statistics
- **Total Agents Ranked:** {data.get('total_agents', 0)}

Great work team!
"""

        else:
            return "Summary generation failed."

    def generate_trend_report(
        self,
        agent_id: str,
        days: int = 30
    ) -> str:
        """Generate trend analysis report.

        Args:
            agent_id: Agent to analyze
            days: Number of days to analyze

        Returns:
            Markdown report
        """
        agent = self.registry.get(agent_id)
        if not agent:
            return f"Agent {agent_id} not found."

        # This would integrate with BigQuery trend analysis
        # For now, return basic info

        return f"""# Trend Analysis - {agent.name}

## Period
Last {days} days

## Metrics
- **Current Success Rate:** {agent.success_rate:.2f}%
- **Current Avg Response Time:** {agent.avg_response_time_ms:.2f}ms
- **Total Tasks (Period):** {agent.total_tasks}

## Trends
_Trend analysis requires historical data integration._

## Recommendations
1. Continue monitoring performance
2. Review any recent changes if metrics decline
3. Consider scaling if load increases
"""
