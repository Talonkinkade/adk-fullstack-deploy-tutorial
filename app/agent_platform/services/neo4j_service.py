"""
Neo4j Service - Database connectivity for context graph.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class Neo4jService:
    """
    Wrapper for Neo4j database operations.

    Handles connection management, query execution, and error handling.
    """

    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        user: str = "neo4j",
        password: str = "password",
    ):
        """
        Initialize Neo4j service.

        Args:
            uri: Neo4j connection URI
            user: Database user
            password: Database password
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        self._initialized = False

    async def connect(self) -> None:
        """Establish connection to Neo4j."""
        try:
            from neo4j import AsyncGraphDatabase

            self.driver = AsyncGraphDatabase.driver(self.uri, auth=(self.user, self.password))

            # Verify connection
            async with self.driver.session() as session:
                result = await session.run("RETURN 1 as test")
                await result.single()

            self._initialized = True
            logger.info(f"Connected to Neo4j at {self.uri}")

        except ImportError:
            logger.warning(
                "neo4j package not installed. Install with: pip install neo4j"
            )
            self._initialized = False

        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self._initialized = False

    async def disconnect(self) -> None:
        """Close Neo4j connection."""
        if self.driver:
            await self.driver.close()
            logger.info("Disconnected from Neo4j")

    async def query(
        self, cypher: str, parameters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Execute a Cypher query.

        Args:
            cypher: Cypher query string
            parameters: Query parameters

        Returns:
            List of result records
        """
        if not self._initialized or not self.driver:
            logger.warning("Neo4j not initialized")
            return []

        try:
            async with self.driver.session() as session:
                result = await session.run(cypher, parameters or {})
                records = await result.values()

                # Convert to list of dicts
                return [dict(zip(result.keys(), record)) for record in records]

        except Exception as e:
            logger.error(f"Query failed: {e}\nQuery: {cypher}", exc_info=True)
            return []

    async def execute(
        self, cypher: str, parameters: dict[str, Any] | None = None
    ) -> None:
        """
        Execute a Cypher command (no return value expected).

        Args:
            cypher: Cypher command string
            parameters: Command parameters
        """
        if not self._initialized or not self.driver:
            logger.warning("Neo4j not initialized")
            return

        try:
            async with self.driver.session() as session:
                await session.run(cypher, parameters or {})

        except Exception as e:
            logger.error(f"Execution failed: {e}\nCommand: {cypher}", exc_info=True)

    async def execute_write(
        self, cypher: str, parameters: dict[str, Any] | None = None
    ) -> Any:
        """
        Execute a write transaction.

        Args:
            cypher: Cypher write command
            parameters: Command parameters

        Returns:
            Result summary
        """
        if not self._initialized or not self.driver:
            logger.warning("Neo4j not initialized")
            return None

        async def _write_tx(tx: Any) -> Any:
            result = await tx.run(cypher, parameters or {})
            return await result.single()

        try:
            async with self.driver.session() as session:
                return await session.execute_write(_write_tx)

        except Exception as e:
            logger.error(f"Write transaction failed: {e}", exc_info=True)
            return None

    async def health_check(self) -> dict[str, Any]:
        """Check database health."""
        if not self._initialized or not self.driver:
            return {"status": "unhealthy", "reason": "Not connected"}

        try:
            async with self.driver.session() as session:
                result = await session.run("RETURN 1 as health")
                await result.single()

            return {"status": "healthy"}

        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    def is_connected(self) -> bool:
        """Check if connected to Neo4j."""
        return self._initialized and self.driver is not None
