"""Neo4j Client - Graph database for agent relationships and workflow dependencies.

Stores:
- Agent dependency graphs
- Workflow relationships
- Task dependencies
- Collaboration networks
- Knowledge graphs
"""

from typing import Any, Dict, List, Optional

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False


class Neo4jClient:
    """Neo4j graph database client for LearnQwest.

    Node types:
    - Agent: Individual agents
    - Task: Task nodes
    - Workflow: Workflow definitions
    - User: User nodes

    Relationship types:
    - DEPENDS_ON: Task/agent dependencies
    - EXECUTES: Agent executes task
    - COLLABORATES_WITH: Agent-agent collaboration
    - PART_OF: Task part of workflow
    - ASSIGNED_TO: Task assigned to agent
    """

    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j client.

        Args:
            uri: Neo4j connection URI
            user: Database user
            password: Database password
        """
        if not NEO4J_AVAILABLE:
            raise ImportError("neo4j driver not installed. Install with: pip install neo4j")

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        """Close the driver."""
        self.driver.close()

    def create_agent_node(
        self,
        agent_id: str,
        properties: Dict[str, Any]
    ) -> bool:
        """Create or update an agent node.

        Args:
            agent_id: Unique agent identifier
            properties: Agent properties (name, tier, capabilities, etc.)

        Returns:
            True if successful
        """
        with self.driver.session() as session:
            result = session.run("""
                MERGE (a:Agent {id: $agent_id})
                SET a += $properties
                RETURN a
            """, agent_id=agent_id, properties=properties)
            return result.single() is not None

    def create_task_node(
        self,
        task_id: str,
        properties: Dict[str, Any]
    ) -> bool:
        """Create or update a task node."""
        with self.driver.session() as session:
            result = session.run("""
                MERGE (t:Task {id: $task_id})
                SET t += $properties
                RETURN t
            """, task_id=task_id, properties=properties)
            return result.single() is not None

    def create_workflow_node(
        self,
        workflow_id: str,
        properties: Dict[str, Any]
    ) -> bool:
        """Create or update a workflow node."""
        with self.driver.session() as session:
            result = session.run("""
                MERGE (w:Workflow {id: $workflow_id})
                SET w += $properties
                RETURN w
            """, workflow_id=workflow_id, properties=properties)
            return result.single() is not None

    def create_dependency(
        self,
        from_id: str,
        from_type: str,
        to_id: str,
        to_type: str,
        relationship_type: str = "DEPENDS_ON",
        properties: Optional[Dict] = None
    ) -> bool:
        """Create a dependency relationship between nodes.

        Args:
            from_id: Source node ID
            from_type: Source node type (Agent, Task, Workflow)
            to_id: Target node ID
            to_type: Target node type
            relationship_type: Type of relationship
            properties: Optional relationship properties

        Returns:
            True if successful
        """
        with self.driver.session() as session:
            query = f"""
                MATCH (a:{from_type} {{id: $from_id}})
                MATCH (b:{to_type} {{id: $to_id}})
                MERGE (a)-[r:{relationship_type}]->(b)
                SET r += $properties
                RETURN r
            """
            result = session.run(
                query,
                from_id=from_id,
                to_id=to_id,
                properties=properties or {}
            )
            return result.single() is not None

    def record_agent_execution(
        self,
        agent_id: str,
        task_id: str,
        properties: Optional[Dict] = None
    ) -> bool:
        """Record that an agent executed a task."""
        return self.create_dependency(
            agent_id, "Agent",
            task_id, "Task",
            "EXECUTES",
            properties
        )

    def record_collaboration(
        self,
        agent_id_1: str,
        agent_id_2: str,
        properties: Optional[Dict] = None
    ) -> bool:
        """Record collaboration between two agents."""
        return self.create_dependency(
            agent_id_1, "Agent",
            agent_id_2, "Agent",
            "COLLABORATES_WITH",
            properties
        )

    def get_agent_dependencies(self, agent_id: str) -> List[Dict]:
        """Get all agents this agent depends on."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Agent {id: $agent_id})-[:DEPENDS_ON]->(b:Agent)
                RETURN b.id as agent_id, b.name as name, b.tier as tier
            """, agent_id=agent_id)
            return [dict(record) for record in result]

    def get_agent_collaborators(self, agent_id: str) -> List[Dict]:
        """Get all agents this agent has collaborated with."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Agent {id: $agent_id})-[r:COLLABORATES_WITH]-(b:Agent)
                RETURN b.id as agent_id, b.name as name, count(r) as collaboration_count
                ORDER BY collaboration_count DESC
            """, agent_id=agent_id)
            return [dict(record) for record in result]

    def get_task_workflow(self, task_id: str) -> Optional[Dict]:
        """Get the workflow a task belongs to."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (t:Task {id: $task_id})-[:PART_OF]->(w:Workflow)
                RETURN w.id as workflow_id, w.name as name
            """, task_id=task_id)
            record = result.single()
            return dict(record) if record else None

    def get_workflow_tasks(self, workflow_id: str) -> List[Dict]:
        """Get all tasks in a workflow."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (t:Task)-[:PART_OF]->(w:Workflow {id: $workflow_id})
                RETURN t.id as task_id, t.name as name, t.status as status
                ORDER BY t.created_at
            """, workflow_id=workflow_id)
            return [dict(record) for record in result]

    def get_agent_task_history(
        self,
        agent_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """Get tasks executed by an agent."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Agent {id: $agent_id})-[r:EXECUTES]->(t:Task)
                RETURN t.id as task_id, t.name as name, t.status as status,
                       r.timestamp as execution_time, r.duration_seconds as duration
                ORDER BY r.timestamp DESC
                LIMIT $limit
            """, agent_id=agent_id, limit=limit)
            return [dict(record) for record in result]

    def find_shortest_path(
        self,
        from_id: str,
        from_type: str,
        to_id: str,
        to_type: str
    ) -> Optional[List[Dict]]:
        """Find shortest path between two nodes.

        Args:
            from_id: Source node ID
            from_type: Source node type
            to_id: Target node ID
            to_type: Target node type

        Returns:
            List of nodes in path, or None if no path exists
        """
        with self.driver.session() as session:
            query = f"""
                MATCH path = shortestPath(
                    (a:{from_type} {{id: $from_id}})-[*]-(b:{to_type} {{id: $to_id}})
                )
                RETURN [node in nodes(path) | {{id: node.id, type: labels(node)[0]}}] as path
            """
            result = session.run(query, from_id=from_id, to_id=to_id)
            record = result.single()
            return record['path'] if record else None

    def get_agent_network_stats(self, agent_id: str) -> Dict:
        """Get network statistics for an agent.

        Returns:
            Dictionary with centrality metrics and collaboration stats
        """
        with self.driver.session() as session:
            # Get degree centrality (number of direct connections)
            degree_result = session.run("""
                MATCH (a:Agent {id: $agent_id})-[r]-(b:Agent)
                RETURN count(DISTINCT b) as degree
            """, agent_id=agent_id)
            degree = degree_result.single()['degree']

            # Get tasks executed
            tasks_result = session.run("""
                MATCH (a:Agent {id: $agent_id})-[:EXECUTES]->(t:Task)
                RETURN count(t) as total_tasks
            """, agent_id=agent_id)
            total_tasks = tasks_result.single()['total_tasks']

            # Get collaborator count
            collab_result = session.run("""
                MATCH (a:Agent {id: $agent_id})-[:COLLABORATES_WITH]-(b:Agent)
                RETURN count(DISTINCT b) as collaborators
            """, agent_id=agent_id)
            collaborators = collab_result.single()['collaborators']

            return {
                "agent_id": agent_id,
                "degree_centrality": degree,
                "total_tasks_executed": total_tasks,
                "unique_collaborators": collaborators,
            }

    def get_most_connected_agents(self, limit: int = 10) -> List[Dict]:
        """Get agents with most connections (highest degree centrality)."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Agent)-[r]-(b:Agent)
                WITH a, count(DISTINCT b) as connections
                RETURN a.id as agent_id, a.name as name, connections
                ORDER BY connections DESC
                LIMIT $limit
            """, limit=limit)
            return [dict(record) for record in result]

    def delete_node(self, node_id: str, node_type: str) -> bool:
        """Delete a node and all its relationships."""
        with self.driver.session() as session:
            result = session.run(f"""
                MATCH (n:{node_type} {{id: $node_id}})
                DETACH DELETE n
                RETURN count(n) as deleted
            """, node_id=node_id)
            return result.single()['deleted'] > 0

    def clear_all_data(self) -> bool:
        """Clear all data from the database. USE WITH CAUTION!"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            return True
