"""
Universal Context Service - Shared knowledge graph for all agents.

Manages the Neo4j context graph where agents store and query information.
Enables cross-domain insights and temporal reasoning.
"""

import logging
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.agent_platform.models.context import (
    ContextNode,
    ContextQuery,
    ContextRelationship,
    ContextType,
    Insight,
    RelationType,
)

logger = logging.getLogger(__name__)


class ContextService:
    """
    Universal context graph service.

    Features:
    - Create/update/query context nodes
    - Create relationships between entities
    - Temporal queries (what happened when)
    - Causal queries (what led to what)
    - Pattern detection
    - Cross-domain insights
    """

    def __init__(self, neo4j_service: Any | None = None):
        """
        Initialize context service.

        Args:
            neo4j_service: Neo4j database service
        """
        self.neo4j = neo4j_service
        self.in_memory_nodes: dict[str, ContextNode] = {}
        self.in_memory_relationships: list[ContextRelationship] = []

    # -------------------------------------------------------------------------
    # Node Operations
    # -------------------------------------------------------------------------

    async def create_node(
        self,
        node_type: ContextType | str,
        label: str,
        properties: dict[str, Any],
        created_by: str | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """
        Create a new context node.

        Args:
            node_type: Type of node (from ContextType enum or custom)
            label: Human-readable label
            properties: Node properties
            created_by: Agent that created this node
            tags: Optional tags for categorization

        Returns:
            The created node ID
        """
        node_id = str(uuid4())
        node = ContextNode(
            node_id=node_id,
            node_type=node_type if isinstance(node_type, ContextType) else ContextType.ENTITY,
            label=label,
            properties=properties,
            created_by=created_by,
            tags=tags or [],
        )

        if self.neo4j:
            await self._persist_node_to_neo4j(node)
        else:
            self.in_memory_nodes[node_id] = node

        logger.debug(f"Created node: {label} ({node_id})")
        return node_id

    async def update_node(
        self, node_id: str, properties: dict[str, Any], merge: bool = True
    ) -> None:
        """
        Update an existing node's properties.

        Args:
            node_id: ID of node to update
            properties: Properties to update
            merge: If True, merge with existing properties; if False, replace
        """
        if self.neo4j:
            if merge:
                query = """
                MATCH (n {node_id: $node_id})
                SET n += $properties, n.updated_at = $updated_at
                RETURN n
                """
            else:
                query = """
                MATCH (n {node_id: $node_id})
                SET n = $properties,
                    n.node_id = $node_id,
                    n.updated_at = $updated_at
                RETURN n
                """

            await self.neo4j.execute(
                query,
                {
                    "node_id": node_id,
                    "properties": properties,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                },
            )

        else:
            if node_id in self.in_memory_nodes:
                node = self.in_memory_nodes[node_id]

                if merge:
                    node.properties.update(properties)
                else:
                    node.properties = properties

                node.updated_at = datetime.now(timezone.utc)

    async def get_node(self, node_id: str) -> ContextNode | None:
        """Get a node by ID."""
        if self.neo4j:
            result = await self.neo4j.query(
                "MATCH (n {node_id: $node_id}) RETURN n", {"node_id": node_id}
            )

            if result:
                return self._deserialize_node(result[0]["n"])
            return None

        else:
            return self.in_memory_nodes.get(node_id)

    async def delete_node(self, node_id: str) -> None:
        """Delete a node and all its relationships."""
        if self.neo4j:
            await self.neo4j.execute(
                "MATCH (n {node_id: $node_id}) DETACH DELETE n", {"node_id": node_id}
            )
        else:
            if node_id in self.in_memory_nodes:
                del self.in_memory_nodes[node_id]

            # Remove relationships
            self.in_memory_relationships = [
                rel
                for rel in self.in_memory_relationships
                if rel.from_node_id != node_id and rel.to_node_id != node_id
            ]

    # -------------------------------------------------------------------------
    # Relationship Operations
    # -------------------------------------------------------------------------

    async def create_relationship(
        self,
        from_node_id: str,
        to_node_id: str,
        relation_type: RelationType | str,
        properties: dict[str, Any] | None = None,
        weight: float = 1.0,
        created_by: str | None = None,
    ) -> None:
        """
        Create a relationship between two nodes.

        Args:
            from_node_id: Source node ID
            to_node_id: Target node ID
            relation_type: Type of relationship
            properties: Optional relationship properties
            weight: Strength of relationship (0.0 to 1.0)
            created_by: Agent that created this relationship
        """
        relationship = ContextRelationship(
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            relation_type=relation_type.value if isinstance(relation_type, RelationType) else relation_type,
            properties=properties or {},
            weight=weight,
            created_by=created_by,
        )

        if self.neo4j:
            await self._persist_relationship_to_neo4j(relationship)
        else:
            self.in_memory_relationships.append(relationship)

        logger.debug(
            f"Created relationship: {from_node_id} -[{relation_type}]-> {to_node_id}"
        )

    async def get_relationships(
        self, node_id: str, direction: str = "both"
    ) -> list[ContextRelationship]:
        """
        Get all relationships for a node.

        Args:
            node_id: Node ID
            direction: "outgoing", "incoming", or "both"

        Returns:
            List of relationships
        """
        if self.neo4j:
            if direction == "outgoing":
                query = "MATCH (n {node_id: $node_id})-[r]->(m) RETURN r, m"
            elif direction == "incoming":
                query = "MATCH (n {node_id: $node_id})<-[r]-(m) RETURN r, m"
            else:
                query = "MATCH (n {node_id: $node_id})-[r]-(m) RETURN r, m"

            results = await self.neo4j.query(query, {"node_id": node_id})
            return [self._deserialize_relationship(r["r"]) for r in results]

        else:
            relationships = []

            for rel in self.in_memory_relationships:
                if direction in ("outgoing", "both") and rel.from_node_id == node_id:
                    relationships.append(rel)
                elif direction in ("incoming", "both") and rel.to_node_id == node_id:
                    relationships.append(rel)

            return relationships

    # -------------------------------------------------------------------------
    # Queries
    # -------------------------------------------------------------------------

    async def query(
        self, cypher: str, parameters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Execute a Cypher query against the context graph.

        Args:
            cypher: Cypher query string
            parameters: Query parameters

        Returns:
            List of result records
        """
        if self.neo4j:
            return await self.neo4j.query(cypher, parameters or {})
        else:
            logger.warning("In-memory mode: Cypher queries not supported")
            return []

    async def find_nodes_by_type(
        self, node_type: ContextType | str, limit: int = 100
    ) -> list[ContextNode]:
        """Find all nodes of a specific type."""
        if self.neo4j:
            query = """
            MATCH (n)
            WHERE n.node_type = $node_type
            RETURN n
            LIMIT $limit
            """

            results = await self.neo4j.query(
                query, {"node_type": str(node_type), "limit": limit}
            )

            return [self._deserialize_node(r["n"]) for r in results]

        else:
            return [
                node
                for node in self.in_memory_nodes.values()
                if node.node_type == node_type
            ][:limit]

    async def find_nodes_by_property(
        self, property_key: str, property_value: Any, limit: int = 100
    ) -> list[ContextNode]:
        """Find nodes with a specific property value."""
        if self.neo4j:
            query = f"""
            MATCH (n)
            WHERE n.{property_key} = $value
            RETURN n
            LIMIT $limit
            """

            results = await self.neo4j.query(query, {"value": property_value, "limit": limit})
            return [self._deserialize_node(r["n"]) for r in results]

        else:
            return [
                node
                for node in self.in_memory_nodes.values()
                if node.properties.get(property_key) == property_value
            ][:limit]

    # -------------------------------------------------------------------------
    # Advanced Queries (Temporal, Causal, Pattern)
    # -------------------------------------------------------------------------

    async def temporal_query(
        self, start_time: datetime, end_time: datetime, node_types: list[str] | None = None
    ) -> list[ContextNode]:
        """
        Query nodes created within a time range.

        Args:
            start_time: Start of time range
            end_time: End of time range
            node_types: Optional filter by node types

        Returns:
            List of nodes created in this time range
        """
        if self.neo4j:
            query = """
            MATCH (n)
            WHERE n.created_at >= $start AND n.created_at <= $end
            """

            if node_types:
                query += " AND n.node_type IN $node_types"

            query += " RETURN n ORDER BY n.created_at"

            results = await self.neo4j.query(
                query,
                {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "node_types": node_types,
                },
            )

            return [self._deserialize_node(r["n"]) for r in results]

        else:
            nodes = [
                node
                for node in self.in_memory_nodes.values()
                if start_time <= node.created_at <= end_time
            ]

            if node_types:
                nodes = [n for n in nodes if n.node_type in node_types]

            return sorted(nodes, key=lambda n: n.created_at)

    async def causal_chain(self, node_id: str, max_depth: int = 5) -> list[ContextNode]:
        """
        Find the causal chain (what led to this node).

        Args:
            node_id: Starting node
            max_depth: Maximum depth to traverse

        Returns:
            List of nodes in the causal chain
        """
        if not self.neo4j:
            return []

        query = """
        MATCH path = (start {node_id: $node_id})<-[:CAUSES*1..]-(cause)
        WHERE length(path) <= $max_depth
        RETURN cause
        ORDER BY length(path)
        """

        results = await self.neo4j.query(
            query, {"node_id": node_id, "max_depth": max_depth}
        )

        return [self._deserialize_node(r["cause"]) for r in results]

    # -------------------------------------------------------------------------
    # Insights & Patterns
    # -------------------------------------------------------------------------

    async def store_insight(self, insight: Insight) -> str:
        """Store a generated insight in the context graph."""
        return await self.create_node(
            node_type=ContextType.INSIGHT,
            label=insight.title,
            properties={
                "description": insight.description,
                "insight_type": insight.insight_type,
                "confidence": insight.confidence,
                "supporting_data": insight.supporting_data,
                "actionable": insight.actionable,
                "actions": insight.actions,
            },
            created_by=insight.generated_by,
        )

    # -------------------------------------------------------------------------
    # Neo4j Persistence Helpers
    # -------------------------------------------------------------------------

    async def _persist_node_to_neo4j(self, node: ContextNode) -> None:
        """Persist a node to Neo4j."""
        if not self.neo4j:
            return

        # Create node with label based on node_type
        label = node.node_type.value.capitalize()

        query = f"""
        CREATE (n:{label} {{
            node_id: $node_id,
            node_type: $node_type,
            label: $label,
            created_at: $created_at,
            updated_at: $updated_at,
            created_by: $created_by,
            tags: $tags
        }})
        SET n += $properties
        RETURN n
        """

        await self.neo4j.execute(
            query,
            {
                "node_id": node.node_id,
                "node_type": node.node_type.value,
                "label": node.label,
                "created_at": node.created_at.isoformat(),
                "updated_at": node.updated_at.isoformat(),
                "created_by": node.created_by,
                "tags": node.tags,
                "properties": node.properties,
            },
        )

    async def _persist_relationship_to_neo4j(
        self, relationship: ContextRelationship
    ) -> None:
        """Persist a relationship to Neo4j."""
        if not self.neo4j:
            return

        query = f"""
        MATCH (from {{node_id: $from_id}})
        MATCH (to {{node_id: $to_id}})
        CREATE (from)-[r:{relationship.relation_type} {{
            weight: $weight,
            created_at: $created_at,
            created_by: $created_by
        }}]->(to)
        SET r += $properties
        RETURN r
        """

        await self.neo4j.execute(
            query,
            {
                "from_id": relationship.from_node_id,
                "to_id": relationship.to_node_id,
                "weight": relationship.weight,
                "created_at": relationship.created_at.isoformat(),
                "created_by": relationship.created_by,
                "properties": relationship.properties,
            },
        )

    @staticmethod
    def _deserialize_node(data: dict[str, Any]) -> ContextNode:
        """Convert Neo4j node data to ContextNode."""
        return ContextNode(
            node_id=data["node_id"],
            node_type=ContextType(data["node_type"]),
            label=data["label"],
            properties={k: v for k, v in data.items() if k not in ["node_id", "node_type", "label", "created_at", "updated_at", "created_by", "tags"]},
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            created_by=data.get("created_by"),
            tags=data.get("tags", []),
        )

    @staticmethod
    def _deserialize_relationship(data: dict[str, Any]) -> ContextRelationship:
        """Convert Neo4j relationship data to ContextRelationship."""
        return ContextRelationship(
            from_node_id=data.get("from_node_id", ""),
            to_node_id=data.get("to_node_id", ""),
            relation_type=data.get("relation_type", ""),
            properties={k: v for k, v in data.items() if k not in ["from_node_id", "to_node_id", "relation_type", "weight", "created_at", "created_by"]},
            weight=data.get("weight", 1.0),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(timezone.utc),
            created_by=data.get("created_by"),
        )

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    async def initialize_schema(self) -> None:
        """Initialize Neo4j schema (indexes, constraints)."""
        if not self.neo4j:
            return

        logger.info("Initializing context graph schema")

        # Create constraints and indexes
        constraints = [
            "CREATE CONSTRAINT node_id_unique IF NOT EXISTS FOR (n:ContextNode) REQUIRE n.node_id IS UNIQUE",
            "CREATE INDEX node_type_idx IF NOT EXISTS FOR (n:ContextNode) ON (n.node_type)",
            "CREATE INDEX created_at_idx IF NOT EXISTS FOR (n:ContextNode) ON (n.created_at)",
        ]

        for constraint in constraints:
            try:
                await self.neo4j.execute(constraint, {})
            except Exception as e:
                logger.warning(f"Could not create constraint/index: {e}")

    async def get_stats(self) -> dict[str, Any]:
        """Get context graph statistics."""
        if self.neo4j:
            node_count_query = "MATCH (n) RETURN count(n) as count"
            rel_count_query = "MATCH ()-[r]->() RETURN count(r) as count"

            node_result = await self.neo4j.query(node_count_query, {})
            rel_result = await self.neo4j.query(rel_count_query, {})

            return {
                "total_nodes": node_result[0]["count"] if node_result else 0,
                "total_relationships": rel_result[0]["count"] if rel_result else 0,
                "mode": "neo4j",
            }
        else:
            return {
                "total_nodes": len(self.in_memory_nodes),
                "total_relationships": len(self.in_memory_relationships),
                "mode": "in_memory",
            }
