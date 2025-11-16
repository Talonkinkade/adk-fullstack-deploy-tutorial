"""
Agent Registry - Discovery and coordination service for all platform agents.

Maintains a live registry of agents, their capabilities, and health status.
Enables dynamic agent discovery and composition.
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any

from app.agent_platform.models.agent import (
    AgentCapability,
    AgentMetadata,
    AgentRegistration,
    AgentStatus,
)

logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    Central registry for all platform agents.

    Features:
    - Agent registration and discovery
    - Capability-based lookup
    - Health monitoring
    - Dependency resolution
    - Agent composition (create teams)
    """

    def __init__(self, neo4j_service: Any | None = None):
        """
        Initialize the agent registry.

        Args:
            neo4j_service: Optional Neo4j service for persistent storage
        """
        self.neo4j = neo4j_service
        self.agents: dict[str, AgentMetadata] = {}  # agent_id -> metadata
        self.agent_instances: dict[str, Any] = {}  # agent_id -> agent instance
        self.running = False
        self._heartbeat_task: asyncio.Task | None = None

    # -------------------------------------------------------------------------
    # Registration
    # -------------------------------------------------------------------------

    async def register(self, registration: AgentRegistration, instance: Any) -> str:
        """
        Register a new agent with the platform.

        Args:
            registration: Agent registration details
            instance: The agent instance

        Returns:
            The assigned agent_id
        """
        agent_id = instance.agent_id
        logger.info(f"Registering agent: {registration.name} ({agent_id})")

        # Create metadata
        metadata = AgentMetadata(
            agent_id=agent_id,
            name=registration.name,
            description=registration.description,
            capabilities=registration.capabilities,
            subscribes_to=registration.subscribes_to,
            publishes=registration.publishes,
            provides_context=registration.provides_context,
            dependencies=registration.dependencies,
            config=registration.config,
            tags=registration.tags,
            status=AgentStatus.READY,
        )

        # Store in memory
        self.agents[agent_id] = metadata
        self.agent_instances[agent_id] = instance

        # Persist to Neo4j if available
        if self.neo4j:
            await self._persist_to_neo4j(metadata)

        logger.info(f"Agent registered successfully: {registration.name}")
        return agent_id

    async def unregister(self, agent_id: str) -> None:
        """Unregister an agent."""
        logger.info(f"Unregistering agent: {agent_id}")

        if agent_id in self.agents:
            del self.agents[agent_id]
        if agent_id in self.agent_instances:
            del self.agent_instances[agent_id]

        if self.neo4j:
            await self.neo4j.execute(
                "MATCH (a:Agent {agent_id: $agent_id}) DETACH DELETE a",
                {"agent_id": agent_id},
            )

    # -------------------------------------------------------------------------
    # Discovery & Lookup
    # -------------------------------------------------------------------------

    async def find_agents_by_capability(
        self, capability_name: str
    ) -> list[AgentMetadata]:
        """
        Find all agents that provide a specific capability.

        Args:
            capability_name: Name of the capability

        Returns:
            List of agents that provide this capability
        """
        matching_agents = []

        for agent in self.agents.values():
            for cap in agent.capabilities:
                if cap.name == capability_name:
                    matching_agents.append(agent)
                    break

        return matching_agents

    async def find_agents_by_tag(self, tag: str) -> list[AgentMetadata]:
        """Find all agents with a specific tag."""
        return [agent for agent in self.agents.values() if tag in agent.tags]

    async def find_agents_by_context(self, context_type: str) -> list[AgentMetadata]:
        """Find all agents that provide a specific context type."""
        return [
            agent
            for agent in self.agents.values()
            if context_type in agent.provides_context
        ]

    async def get_agent(self, agent_id: str) -> AgentMetadata | None:
        """Get metadata for a specific agent."""
        return self.agents.get(agent_id)

    async def get_agent_instance(self, agent_id: str) -> Any | None:
        """Get the actual agent instance."""
        return self.agent_instances.get(agent_id)

    async def list_agents(
        self, status: AgentStatus | None = None
    ) -> list[AgentMetadata]:
        """
        List all registered agents.

        Args:
            status: Optional filter by status

        Returns:
            List of agent metadata
        """
        agents = list(self.agents.values())

        if status:
            agents = [a for a in agents if a.status == status]

        return agents

    # -------------------------------------------------------------------------
    # Agent Composition (Team Building)
    # -------------------------------------------------------------------------

    async def compose_team(
        self, required_capabilities: list[str], preferred_tags: list[str] | None = None
    ) -> list[AgentMetadata]:
        """
        Compose a team of agents based on required capabilities.

        This enables dynamic agent team creation for complex tasks.

        Args:
            required_capabilities: Capabilities needed for the task
            preferred_tags: Optional tags to prefer when selecting agents

        Returns:
            List of agents that together provide all required capabilities
        """
        team: list[AgentMetadata] = []
        covered_capabilities: set[str] = set()

        # First pass: select agents with preferred tags
        if preferred_tags:
            for agent in self.agents.values():
                if any(tag in agent.tags for tag in preferred_tags):
                    agent_caps = {cap.name for cap in agent.capabilities}
                    new_caps = agent_caps - covered_capabilities

                    if new_caps:
                        team.append(agent)
                        covered_capabilities.update(new_caps)

        # Second pass: fill in missing capabilities
        for capability in required_capabilities:
            if capability not in covered_capabilities:
                agents = await self.find_agents_by_capability(capability)

                if agents:
                    # Pick the healthiest agent
                    best_agent = max(agents, key=lambda a: a.health_score)
                    team.append(best_agent)
                    covered_capabilities.add(capability)

        logger.info(
            f"Composed team of {len(team)} agents for capabilities: {required_capabilities}"
        )
        return team

    # -------------------------------------------------------------------------
    # Health Monitoring
    # -------------------------------------------------------------------------

    async def update_health(
        self, agent_id: str, health_score: float, metrics: dict[str, Any] | None = None
    ) -> None:
        """
        Update agent health score.

        Args:
            agent_id: Agent to update
            health_score: Health score (0.0 to 1.0)
            metrics: Optional additional metrics
        """
        if agent_id in self.agents:
            self.agents[agent_id].health_score = health_score
            self.agents[agent_id].last_heartbeat = datetime.now(timezone.utc)

            if metrics:
                # Update metrics
                agent = self.agents[agent_id]
                if "events_processed" in metrics:
                    agent.total_events_processed = metrics["events_processed"]
                if "average_response_time_ms" in metrics:
                    agent.average_response_time_ms = metrics["average_response_time_ms"]

    async def _heartbeat_monitor(self) -> None:
        """Monitor agent heartbeats and update health."""
        while self.running:
            try:
                now = datetime.now(timezone.utc)

                for agent_id, agent in self.agents.items():
                    # Check if agent has sent heartbeat recently
                    time_since_heartbeat = (now - agent.last_heartbeat).total_seconds()

                    if time_since_heartbeat > 60:  # No heartbeat for 1 minute
                        # Reduce health score
                        agent.health_score = max(0.0, agent.health_score - 0.1)

                        if agent.health_score < 0.5:
                            agent.status = AgentStatus.ERROR
                            logger.warning(
                                f"Agent {agent.name} health degraded: {agent.health_score}"
                            )

                await asyncio.sleep(30)  # Check every 30 seconds

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in heartbeat monitor: {e}", exc_info=True)

    # -------------------------------------------------------------------------
    # Neo4j Persistence
    # -------------------------------------------------------------------------

    async def _persist_to_neo4j(self, metadata: AgentMetadata) -> None:
        """Persist agent metadata to Neo4j."""
        if not self.neo4j:
            return

        query = """
        MERGE (a:Agent {agent_id: $agent_id})
        SET a.name = $name,
            a.description = $description,
            a.version = $version,
            a.status = $status,
            a.health_score = $health_score,
            a.last_heartbeat = $last_heartbeat,
            a.tags = $tags
        RETURN a
        """

        await self.neo4j.execute(
            query,
            {
                "agent_id": metadata.agent_id,
                "name": metadata.name,
                "description": metadata.description,
                "version": metadata.version,
                "status": metadata.status.value,
                "health_score": metadata.health_score,
                "last_heartbeat": metadata.last_heartbeat.isoformat(),
                "tags": metadata.tags,
            },
        )

        # Create capability nodes and relationships
        for capability in metadata.capabilities:
            cap_query = """
            MATCH (a:Agent {agent_id: $agent_id})
            MERGE (c:Capability {name: $cap_name})
            SET c.description = $cap_description
            MERGE (a)-[:PROVIDES]->(c)
            """

            await self.neo4j.execute(
                cap_query,
                {
                    "agent_id": metadata.agent_id,
                    "cap_name": capability.name,
                    "cap_description": capability.description,
                },
            )

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    async def start(self) -> None:
        """Start the registry and health monitoring."""
        logger.info("Starting agent registry")
        self.running = True
        self._heartbeat_task = asyncio.create_task(self._heartbeat_monitor())

    async def stop(self) -> None:
        """Stop the registry."""
        logger.info("Stopping agent registry")
        self.running = False

        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------

    async def get_stats(self) -> dict[str, Any]:
        """Get registry statistics."""
        total_agents = len(self.agents)
        status_counts = {}

        for status in AgentStatus:
            status_counts[status.value] = sum(
                1 for a in self.agents.values() if a.status == status
            )

        total_capabilities = sum(len(a.capabilities) for a in self.agents.values())

        return {
            "total_agents": total_agents,
            "status_breakdown": status_counts,
            "total_capabilities": total_capabilities,
            "average_health_score": (
                sum(a.health_score for a in self.agents.values()) / total_agents
                if total_agents > 0
                else 0.0
            ),
        }
