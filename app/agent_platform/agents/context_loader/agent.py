"""
Context Loader Agent - Automates context retrieval and sharing.

This agent loads context from various sources and makes it available
to other agents through the universal context graph.
"""

import json
import logging
from pathlib import Path
from typing import Any

from app.agent_platform.core.base_agent import BaseAgent
from app.agent_platform.models.agent import AgentCapability
from app.agent_platform.models.context import ContextType, RelationType
from app.agent_platform.models.events import BaseEvent

logger = logging.getLogger(__name__)


class ContextLoaderAgent(BaseAgent):
    """
    Loads and manages context from multiple sources.

    Capabilities:
    - Load context from files (JSON, YAML, Markdown)
    - Monitor directories for context changes
    - Sync context across agents
    - Build knowledge graph from structured data
    """

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(
            name="context_loader",
            description="Automates context retrieval and sharing across all projects and team tools",
            version="1.0.0",
            config=config or {},
        )

        self.context_sources = self.config.get("context_sources", [])
        self.auto_sync = self.config.get("auto_sync", True)

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    async def setup(self) -> None:
        """Setup the agent."""
        logger.info("Setting up Context Loader Agent")

        # Subscribe to context requests
        await self.subscribe("context.load_request", self._handle_load_request)
        await self.subscribe("context.sync_request", self._handle_sync_request)

        # Load initial context if configured
        if self.auto_sync:
            await self.load_all_contexts()

    async def process_event(self, event: BaseEvent) -> None:
        """Process incoming events."""
        if event.event_type == "context.load_request":
            await self._handle_load_request(event)
        elif event.event_type == "context.sync_request":
            await self._handle_sync_request(event)

    # -------------------------------------------------------------------------
    # Capabilities
    # -------------------------------------------------------------------------

    def get_capabilities(self) -> list[AgentCapability]:
        """Declare agent capabilities."""
        return [
            AgentCapability(
                name="load_context",
                description="Load context from various sources (files, APIs, databases)",
                input_schema={
                    "type": "object",
                    "properties": {
                        "source_type": {"type": "string"},
                        "source_path": {"type": "string"},
                    },
                },
            ),
            AgentCapability(
                name="sync_context",
                description="Synchronize context across the platform",
            ),
        ]

    # -------------------------------------------------------------------------
    # Context Loading
    # -------------------------------------------------------------------------

    async def load_all_contexts(self) -> None:
        """Load context from all configured sources."""
        logger.info(f"Loading context from {len(self.context_sources)} sources")

        for source in self.context_sources:
            try:
                await self.load_context(source["type"], source["path"])
            except Exception as e:
                logger.error(f"Failed to load context from {source}: {e}")

        await self.publish_event(
            "context.loaded",
            {
                "sources_count": len(self.context_sources),
                "status": "completed",
            },
        )

    async def load_context(self, source_type: str, source_path: str) -> None:
        """
        Load context from a specific source.

        Args:
            source_type: Type of source ("file", "api", "database")
            source_path: Path or identifier for the source
        """
        logger.info(f"Loading context from {source_type}: {source_path}")

        if source_type == "file":
            await self._load_from_file(source_path)
        elif source_type == "api":
            await self._load_from_api(source_path)
        elif source_type == "database":
            await self._load_from_database(source_path)

    async def _load_from_file(self, file_path: str) -> None:
        """Load context from a file."""
        path = Path(file_path)

        if not path.exists():
            logger.warning(f"File not found: {file_path}")
            return

        # Determine file type and load accordingly
        if path.suffix in [".json", ".jsonl"]:
            await self._load_json_file(path)
        elif path.suffix in [".yaml", ".yml"]:
            await self._load_yaml_file(path)
        elif path.suffix == ".md":
            await self._load_markdown_file(path)

    async def _load_json_file(self, path: Path) -> None:
        """Load context from JSON file."""
        try:
            with open(path, "r") as f:
                data = json.load(f)

            # Create context node
            node_id = await self.update_context(
                node_type="entity",
                properties={
                    "source_file": str(path),
                    "data": data,
                    "loaded_at": self.metadata.last_heartbeat.isoformat(),
                },
            )

            logger.info(f"Loaded JSON context from {path}: node_id={node_id}")

        except Exception as e:
            logger.error(f"Failed to load JSON file {path}: {e}")

    async def _load_yaml_file(self, path: Path) -> None:
        """Load context from YAML file."""
        try:
            import yaml

            with open(path, "r") as f:
                data = yaml.safe_load(f)

            # Create context node
            node_id = await self.update_context(
                node_type="entity",
                properties={
                    "source_file": str(path),
                    "data": data,
                    "loaded_at": self.metadata.last_heartbeat.isoformat(),
                },
            )

            logger.info(f"Loaded YAML context from {path}: node_id={node_id}")

        except ImportError:
            logger.warning("PyYAML not installed. Install with: pip install pyyaml")
        except Exception as e:
            logger.error(f"Failed to load YAML file {path}: {e}")

    async def _load_markdown_file(self, path: Path) -> None:
        """Load context from Markdown file (e.g., knowledge base notes)."""
        try:
            with open(path, "r") as f:
                content = f.read()

            # Create context node for the document
            node_id = await self.update_context(
                node_type=ContextType.JOURNAL_ENTRY.value,
                properties={
                    "source_file": str(path),
                    "content": content,
                    "title": path.stem,
                    "loaded_at": self.metadata.last_heartbeat.isoformat(),
                },
            )

            logger.info(f"Loaded Markdown context from {path}: node_id={node_id}")

        except Exception as e:
            logger.error(f"Failed to load Markdown file {path}: {e}")

    async def _load_from_api(self, api_url: str) -> None:
        """Load context from an API."""
        # Placeholder for API integration
        logger.info(f"Loading context from API: {api_url}")
        # TODO: Implement API fetching with requests/httpx

    async def _load_from_database(self, db_path: str) -> None:
        """Load context from a database."""
        # Placeholder for database integration
        logger.info(f"Loading context from database: {db_path}")
        # TODO: Implement database querying

    # -------------------------------------------------------------------------
    # Event Handlers
    # -------------------------------------------------------------------------

    async def _handle_load_request(self, event: BaseEvent) -> None:
        """Handle context load requests from other agents."""
        source_type = event.data.get("source_type")
        source_path = event.data.get("source_path")

        if source_type and source_path:
            await self.load_context(source_type, source_path)

    async def _handle_sync_request(self, event: BaseEvent) -> None:
        """Handle context sync requests."""
        await self.load_all_contexts()
