"""
Redis Service - Message broker and caching for the platform.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class RedisService:
    """
    Wrapper for Redis operations.

    Handles connection management, stream operations, and pub/sub.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
    ):
        """
        Initialize Redis service.

        Args:
            host: Redis host
            port: Redis port
            db: Database number
            password: Optional password
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client = None
        self._initialized = False

    async def connect(self) -> None:
        """Establish connection to Redis."""
        try:
            import redis.asyncio as redis

            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True,
            )

            # Verify connection
            await self.client.ping()

            self._initialized = True
            logger.info(f"Connected to Redis at {self.host}:{self.port}")

        except ImportError:
            logger.warning(
                "redis package not installed. Install with: pip install redis"
            )
            self._initialized = False

        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self._initialized = False

    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self.client:
            await self.client.close()
            logger.info("Disconnected from Redis")

    # -------------------------------------------------------------------------
    # Stream Operations (for Event Bus)
    # -------------------------------------------------------------------------

    async def xadd(self, stream: str, fields: dict[str, Any]) -> str:
        """Add entry to stream."""
        if not self._initialized or not self.client:
            logger.warning("Redis not initialized")
            return ""

        try:
            return await self.client.xadd(stream, fields)
        except Exception as e:
            logger.error(f"xadd failed: {e}", exc_info=True)
            return ""

    async def xread(
        self, streams: dict[str, str], count: int | None = None, block: int | None = None
    ) -> list[tuple[str, list[tuple[str, dict]]]]:
        """Read from streams."""
        if not self._initialized or not self.client:
            return []

        try:
            return await self.client.xread(streams, count=count, block=block)
        except Exception as e:
            logger.error(f"xread failed: {e}", exc_info=True)
            return []

    async def xgroup_create(
        self, stream: str, group: str, id: str = "0", mkstream: bool = False
    ) -> bool:
        """Create consumer group."""
        if not self._initialized or not self.client:
            return False

        try:
            await self.client.xgroup_create(stream, group, id=id, mkstream=mkstream)
            return True
        except Exception as e:
            # Group might already exist
            if "BUSYGROUP" not in str(e):
                logger.error(f"xgroup_create failed: {e}", exc_info=True)
            return False

    async def xreadgroup(
        self,
        group: str,
        consumer: str,
        streams: dict[str, str],
        count: int | None = None,
        block: int | None = None,
    ) -> list[tuple[str, list[tuple[str, dict]]]]:
        """Read from stream as consumer group member."""
        if not self._initialized or not self.client:
            return []

        try:
            return await self.client.xreadgroup(
                group, consumer, streams, count=count, block=block
            )
        except Exception as e:
            logger.error(f"xreadgroup failed: {e}", exc_info=True)
            return []

    async def xack(self, stream: str, group: str, *ids: str) -> int:
        """Acknowledge messages."""
        if not self._initialized or not self.client:
            return 0

        try:
            return await self.client.xack(stream, group, *ids)
        except Exception as e:
            logger.error(f"xack failed: {e}", exc_info=True)
            return 0

    async def xrange(
        self, stream: str, min: str = "-", max: str = "+", count: int | None = None
    ) -> list[tuple[str, dict]]:
        """Get range of entries from stream."""
        if not self._initialized or not self.client:
            return []

        try:
            return await self.client.xrange(stream, min=min, max=max, count=count)
        except Exception as e:
            logger.error(f"xrange failed: {e}", exc_info=True)
            return []

    # -------------------------------------------------------------------------
    # Key-Value Operations (for caching)
    # -------------------------------------------------------------------------

    async def get(self, key: str) -> str | None:
        """Get value by key."""
        if not self._initialized or not self.client:
            return None

        try:
            return await self.client.get(key)
        except Exception as e:
            logger.error(f"get failed: {e}", exc_info=True)
            return None

    async def set(
        self, key: str, value: str, ex: int | None = None
    ) -> bool:
        """Set key-value pair."""
        if not self._initialized or not self.client:
            return False

        try:
            await self.client.set(key, value, ex=ex)
            return True
        except Exception as e:
            logger.error(f"set failed: {e}", exc_info=True)
            return False

    async def delete(self, *keys: str) -> int:
        """Delete keys."""
        if not self._initialized or not self.client:
            return 0

        try:
            return await self.client.delete(*keys)
        except Exception as e:
            logger.error(f"delete failed: {e}", exc_info=True)
            return 0

    # -------------------------------------------------------------------------
    # Health
    # -------------------------------------------------------------------------

    async def health_check(self) -> dict[str, Any]:
        """Check Redis health."""
        if not self._initialized or not self.client:
            return {"status": "unhealthy", "reason": "Not connected"}

        try:
            await self.client.ping()
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    def is_connected(self) -> bool:
        """Check if connected to Redis."""
        return self._initialized and self.client is not None
