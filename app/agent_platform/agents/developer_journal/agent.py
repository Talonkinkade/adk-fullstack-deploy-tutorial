"""
Developer Journal Agent - Automated learning and troubleshooting log.

This agent prompts for daily entries, organizes learning history,
and builds a searchable knowledge base of development experiences.
"""

import logging
from datetime import datetime, timezone
from typing import Any

from app.agent_platform.core.base_agent import BaseAgent
from app.agent_platform.models.agent import AgentCapability
from app.agent_platform.models.context import ContextType, RelationType
from app.agent_platform.models.events import BaseEvent, EventPriority

logger = logging.getLogger(__name__)


class DeveloperJournalAgent(BaseAgent):
    """
    Manages developer journaling and knowledge capture.

    Capabilities:
    - Daily prompts for journal entries
    - Log learnings, bugs, solutions
    - Build searchable knowledge graph
    - Generate weekly/monthly summaries
    - Track skill progression
    """

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(
            name="developer_journal",
            description="Prompts daily, logs entries, organizes learning and troubleshooting history",
            version="1.0.0",
            config=config or {},
        )

        self.prompt_time = self.config.get("prompt_time", "09:00")  # Daily prompt time
        self.auto_summarize = self.config.get("auto_summarize", True)

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    async def setup(self) -> None:
        """Setup the agent."""
        logger.info("Setting up Developer Journal Agent")

        # Subscribe to relevant events
        await self.subscribe("user.journal_entry", self._handle_journal_entry)
        await self.subscribe("schedule.daily_trigger", self._handle_daily_prompt)

        # Send initial prompt
        await self.send_daily_prompt()

    async def process_event(self, event: BaseEvent) -> None:
        """Process incoming events."""
        if event.event_type == "user.journal_entry":
            await self._handle_journal_entry(event)
        elif event.event_type == "schedule.daily_trigger":
            await self._handle_daily_prompt(event)

    # -------------------------------------------------------------------------
    # Capabilities
    # -------------------------------------------------------------------------

    def get_capabilities(self) -> list[AgentCapability]:
        """Declare agent capabilities."""
        return [
            AgentCapability(
                name="create_journal_entry",
                description="Create and store a developer journal entry",
                input_schema={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "content": {"type": "string"},
                        "tags": {"type": "array", "items": {"type": "string"}},
                        "category": {"type": "string"},
                    },
                    "required": ["content"],
                },
            ),
            AgentCapability(
                name="search_journal",
                description="Search through journal entries",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "tags": {"type": "array"},
                        "date_range": {"type": "object"},
                    },
                },
            ),
            AgentCapability(
                name="generate_summary",
                description="Generate summary of journal entries for a time period",
            ),
        ]

    # -------------------------------------------------------------------------
    # Journal Entry Management
    # -------------------------------------------------------------------------

    async def create_entry(
        self,
        content: str,
        title: str | None = None,
        tags: list[str] | None = None,
        category: str = "general",
        learnings: list[str] | None = None,
        problems: list[str] | None = None,
        solutions: list[str] | None = None,
    ) -> str:
        """
        Create a new journal entry.

        Args:
            content: Main content of the entry
            title: Optional title
            tags: Optional tags for categorization
            category: Category (general, bug, learning, achievement)
            learnings: List of things learned
            problems: List of problems encountered
            solutions: List of solutions found

        Returns:
            Entry node ID
        """
        timestamp = datetime.now(timezone.utc)

        entry_data = {
            "content": content,
            "title": title or f"Entry {timestamp.strftime('%Y-%m-%d %H:%M')}",
            "category": category,
            "timestamp": timestamp.isoformat(),
            "tags": tags or [],
        }

        if learnings:
            entry_data["learnings"] = learnings
        if problems:
            entry_data["problems"] = problems
        if solutions:
            entry_data["solutions"] = solutions

        # Create context node
        entry_id = await self.update_context(
            node_type=ContextType.JOURNAL_ENTRY.value,
            properties=entry_data,
        )

        # Create relationships to skills if learnings mentioned
        if learnings:
            await self._link_to_skills(entry_id, learnings)

        logger.info(f"Created journal entry: {entry_id}")

        # Publish event
        await self.publish_event(
            "journal.entry_created",
            {"entry_id": entry_id, "title": entry_data["title"], "category": category},
        )

        return entry_id

    async def _link_to_skills(self, entry_id: str, learnings: list[str]) -> None:
        """Link journal entry to skills learned."""
        for learning in learnings:
            # Find or create skill node
            skill_nodes = await self.query_context(
                """
                MATCH (s:Skill)
                WHERE toLower(s.name) CONTAINS toLower($learning)
                RETURN s.node_id as node_id
                LIMIT 1
                """,
                {"learning": learning},
            )

            if skill_nodes:
                skill_id = skill_nodes[0]["node_id"]
            else:
                # Create new skill node
                skill_id = await self.update_context(
                    node_type=ContextType.SKILL.value,
                    properties={"name": learning, "level": "beginner"},
                )

            # Create relationship
            await self.create_relationship(
                entry_id,
                skill_id,
                RelationType.RELATED_TO.value,
                {"learning_occurred": True},
            )

    async def search_entries(
        self,
        query: str | None = None,
        tags: list[str] | None = None,
        category: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search journal entries."""
        cypher_parts = ["MATCH (e:JournalEntry)"]
        conditions = []
        params: dict[str, Any] = {"limit": limit}

        if query:
            conditions.append("e.content CONTAINS $query OR e.title CONTAINS $query")
            params["query"] = query

        if tags:
            conditions.append("ANY(tag IN $tags WHERE tag IN e.tags)")
            params["tags"] = tags

        if category:
            conditions.append("e.category = $category")
            params["category"] = category

        if conditions:
            cypher_parts.append("WHERE " + " AND ".join(conditions))

        cypher_parts.append("RETURN e ORDER BY e.timestamp DESC LIMIT $limit")

        cypher = " ".join(cypher_parts)
        results = await self.query_context(cypher, params)

        return results

    # -------------------------------------------------------------------------
    # Daily Prompts & Summaries
    # -------------------------------------------------------------------------

    async def send_daily_prompt(self) -> None:
        """Send daily journaling prompt to user."""
        prompt = """
📝 **Daily Developer Journal Prompt**

Take a moment to reflect on your day:

- What did you work on today?
- What did you learn?
- What challenges did you face?
- What solutions did you discover?
- Any insights or aha moments?

Type your journal entry or say "skip" to skip today.
        """

        await self.send_notification(prompt, priority=EventPriority.NORMAL)

    async def _handle_daily_prompt(self, event: BaseEvent) -> None:
        """Handle scheduled daily prompt."""
        await self.send_daily_prompt()

    async def _handle_journal_entry(self, event: BaseEvent) -> None:
        """Handle user journal entry submission."""
        content = event.data.get("content", "")
        title = event.data.get("title")
        tags = event.data.get("tags", [])
        category = event.data.get("category", "general")

        if content and content.lower() != "skip":
            await self.create_entry(
                content=content, title=title, tags=tags, category=category
            )

    async def generate_weekly_summary(self) -> str:
        """Generate summary of the past week's entries."""
        # Query last week's entries
        entries = await self.query_context(
            """
            MATCH (e:JournalEntry)
            WHERE e.timestamp > datetime() - duration({days: 7})
            RETURN e
            ORDER BY e.timestamp DESC
            """,
            {},
        )

        if not entries:
            return "No journal entries in the past week."

        # Generate summary
        summary_parts = [
            "📊 **Weekly Journal Summary**\n",
            f"Total entries: {len(entries)}\n\n",
        ]

        # Categorize entries
        categories: dict[str, int] = {}
        all_tags: set[str] = set()

        for entry_data in entries:
            entry = entry_data.get("e", {})
            cat = entry.get("category", "general")
            categories[cat] = categories.get(cat, 0) + 1

            for tag in entry.get("tags", []):
                all_tags.add(tag)

        summary_parts.append("**Breakdown by category:**\n")
        for cat, count in categories.items():
            summary_parts.append(f"- {cat}: {count}\n")

        if all_tags:
            summary_parts.append(f"\n**Tags:** {', '.join(sorted(all_tags))}\n")

        summary = "".join(summary_parts)

        # Store summary as an insight
        if self.context_service:
            await self.context_service.create_node(
                node_type=ContextType.INSIGHT,
                label="Weekly Journal Summary",
                properties={
                    "summary": summary,
                    "period": "week",
                    "entry_count": len(entries),
                },
                created_by=self.name,
            )

        return summary
