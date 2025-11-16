"""
Agent Platform Orchestrator - Wires all components together.

This is the main entry point for running the autonomous agent platform.
"""

import asyncio
import logging
import os
from typing import Any

from app.agent_platform.core.base_agent import BaseAgent
from app.agent_platform.core.context import ContextService
from app.agent_platform.core.event_bus import EventBus
from app.agent_platform.core.registry import AgentRegistry
from app.agent_platform.services.neo4j_service import Neo4jService
from app.agent_platform.services.redis_service import RedisService

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AgentPlatform:
    """
    Main platform orchestrator.

    Responsibilities:
    - Initialize core services (Neo4j, Redis)
    - Create and wire platform components (Event Bus, Registry, Context)
    - Manage agent lifecycle
    - Provide platform-wide health monitoring
    """

    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize the agent platform.

        Args:
            config: Platform configuration
        """
        self.config = config or {}

        # Services
        self.neo4j_service: Neo4jService | None = None
        self.redis_service: RedisService | None = None

        # Core components
        self.event_bus: EventBus | None = None
        self.registry: AgentRegistry | None = None
        self.context_service: ContextService | None = None

        # Agents
        self.agents: list[BaseAgent] = []

        # State
        self.running = False

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------

    async def initialize(self) -> None:
        """Initialize all platform components."""
        logger.info("🚀 Initializing Agent Platform...")

        # Initialize services
        await self._init_services()

        # Initialize core components
        await self._init_core_components()

        logger.info("✅ Agent Platform initialized successfully!")

    async def _init_services(self) -> None:
        """Initialize external services (Neo4j, Redis)."""
        # Neo4j (optional - will use in-memory mode if not available)
        neo4j_uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.environ.get("NEO4J_USER", "neo4j")
        neo4j_password = os.environ.get("NEO4J_PASSWORD", "password")

        self.neo4j_service = Neo4jService(neo4j_uri, neo4j_user, neo4j_password)
        await self.neo4j_service.connect()

        if not self.neo4j_service.is_connected():
            logger.warning(
                "⚠️  Neo4j not available - using in-memory mode (context won't persist)"
            )
            self.neo4j_service = None

        # Redis (optional - will use in-memory mode if not available)
        redis_host = os.environ.get("REDIS_HOST", "localhost")
        redis_port = int(os.environ.get("REDIS_PORT", "6379"))
        redis_password = os.environ.get("REDIS_PASSWORD")

        self.redis_service = RedisService(redis_host, redis_port, password=redis_password)
        await self.redis_service.connect()

        if not self.redis_service.is_connected():
            logger.warning(
                "⚠️  Redis not available - using in-memory event bus (events won't distribute)"
            )
            self.redis_service = None

    async def _init_core_components(self) -> None:
        """Initialize core platform components."""
        # Event Bus
        self.event_bus = EventBus(
            redis_client=self.redis_service.client if self.redis_service else None
        )
        await self.event_bus.start()

        # Agent Registry
        self.registry = AgentRegistry(neo4j_service=self.neo4j_service)
        await self.registry.start()

        # Context Service
        self.context_service = ContextService(neo4j_service=self.neo4j_service)

        if self.neo4j_service:
            await self.context_service.initialize_schema()

    # -------------------------------------------------------------------------
    # Agent Management
    # -------------------------------------------------------------------------

    async def register_agent(self, agent: BaseAgent) -> None:
        """
        Register and start an agent.

        Args:
            agent: Agent instance to register
        """
        logger.info(f"Registering agent: {agent.name}")

        # Inject platform services
        agent.event_bus = self.event_bus
        agent.context_service = self.context_service
        agent.registry = self.registry

        # Start the agent
        await agent.start()

        # Track agent
        self.agents.append(agent)

    async def unregister_agent(self, agent_id: str) -> None:
        """Unregister and stop an agent."""
        agent = next((a for a in self.agents if a.agent_id == agent_id), None)

        if agent:
            await agent.stop()
            self.agents.remove(agent)

            if self.registry:
                await self.registry.unregister(agent_id)

    async def get_agent(self, name: str) -> BaseAgent | None:
        """Get agent by name."""
        return next((a for a in self.agents if a.name == name), None)

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    async def start(self) -> None:
        """Start the platform."""
        logger.info("🔄 Starting Agent Platform...")
        self.running = True

        # Platform is now ready to accept agents
        logger.info("✅ Agent Platform is running!")

    async def stop(self) -> None:
        """Stop the platform and cleanup."""
        logger.info("🛑 Stopping Agent Platform...")
        self.running = False

        # Stop all agents
        for agent in self.agents:
            await agent.stop()

        # Stop core components
        if self.event_bus:
            await self.event_bus.stop()

        if self.registry:
            await self.registry.stop()

        # Disconnect services
        if self.neo4j_service:
            await self.neo4j_service.disconnect()

        if self.redis_service:
            await self.redis_service.disconnect()

        logger.info("✅ Agent Platform stopped successfully!")

    # -------------------------------------------------------------------------
    # Health & Monitoring
    # -------------------------------------------------------------------------

    async def health_check(self) -> dict[str, Any]:
        """Comprehensive platform health check."""
        health = {
            "platform": "running" if self.running else "stopped",
            "services": {},
            "components": {},
            "agents": {},
        }

        # Check services
        if self.neo4j_service:
            health["services"]["neo4j"] = await self.neo4j_service.health_check()
        else:
            health["services"]["neo4j"] = {"status": "disabled"}

        if self.redis_service:
            health["services"]["redis"] = await self.redis_service.health_check()
        else:
            health["services"]["redis"] = {"status": "disabled"}

        # Check components
        if self.event_bus:
            health["components"]["event_bus"] = await self.event_bus.get_stats()

        if self.registry:
            health["components"]["registry"] = await self.registry.get_stats()

        if self.context_service:
            health["components"]["context"] = await self.context_service.get_stats()

        # Check agents
        for agent in self.agents:
            health["agents"][agent.name] = await agent.health_check()

        return health

    async def get_platform_stats(self) -> dict[str, Any]:
        """Get comprehensive platform statistics."""
        stats = {
            "total_agents": len(self.agents),
            "running": self.running,
        }

        if self.event_bus:
            stats["event_bus"] = await self.event_bus.get_stats()

        if self.registry:
            stats["registry"] = await self.registry.get_stats()

        if self.context_service:
            stats["context"] = await self.context_service.get_stats()

        return stats

    # -------------------------------------------------------------------------
    # Utilities
    # -------------------------------------------------------------------------

    async def broadcast_notification(self, message: str) -> None:
        """Send notification to all users via all agents."""
        if self.event_bus:
            from app.agent_platform.models.events import BaseEvent, EventPriority

            event = BaseEvent(
                event_type="user.notification",
                source_agent="platform",
                data={"message": message},
                priority=EventPriority.HIGH,
            )

            await self.event_bus.publish(event)


# =============================================================================
# Platform Singleton & Helpers
# =============================================================================

_platform_instance: AgentPlatform | None = None


async def get_platform() -> AgentPlatform:
    """Get or create the platform singleton."""
    global _platform_instance

    if _platform_instance is None:
        _platform_instance = AgentPlatform()
        await _platform_instance.initialize()
        await _platform_instance.start()

    return _platform_instance


async def shutdown_platform() -> None:
    """Shutdown the platform singleton."""
    global _platform_instance

    if _platform_instance:
        await _platform_instance.stop()
        _platform_instance = None


# =============================================================================
# Example Usage
# =============================================================================

async def main() -> None:
    """Example: Start the platform and run indefinitely."""
    platform = await get_platform()

    try:
        # Platform is running
        logger.info("Platform ready. Press Ctrl+C to stop.")

        # Keep alive
        while platform.running:
            await asyncio.sleep(1)

            # Periodic health check
            if int(asyncio.get_event_loop().time()) % 60 == 0:
                health = await platform.health_check()
                logger.info(f"Health: {health['platform']}")

    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
    finally:
        await shutdown_platform()


if __name__ == "__main__":
    asyncio.run(main())
