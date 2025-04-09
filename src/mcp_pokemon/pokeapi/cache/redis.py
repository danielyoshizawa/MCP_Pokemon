"""Redis cache implementation."""

from typing import Optional
import redis.asyncio as redis

from mcp_pokemon.pokeapi.cache.base import CacheProvider


class RedisCache(CacheProvider):
    """Redis implementation of the cache provider."""

    def __init__(self, redis_url: str) -> None:
        """Initialize the Redis cache.
        
        Args:
            redis_url: The URL to connect to Redis.
        """
        self.redis_url = redis_url
        self._client: Optional[redis.Redis] = None

    @property
    def client(self) -> redis.Redis:
        """Get the Redis client.
        
        Returns:
            The Redis client.
            
        Raises:
            ConnectionError: If the client is not connected.
        """
        if self._client is None:
            raise ConnectionError("Redis client is not connected")
        return self._client

    async def connect(self) -> None:
        """Connect to the Redis server."""
        if self._client is None:
            self._client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            # Test connection
            await self._client.ping()

    async def close(self) -> None:
        """Close the connection to the Redis server."""
        if self._client is not None:
            await self._client.close()
            self._client = None

    async def get(self, key: str) -> Optional[str]:
        """Get a value from the cache.
        
        Args:
            key: The key to get the value for.
            
        Returns:
            The cached value if it exists, None otherwise.
        """
        return await self.client.get(key)

    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        """Set a value in the cache.
        
        Args:
            key: The key to set the value for.
            value: The value to cache.
            ttl: Time to live in seconds. If None, the value will not expire.
        """
        await self.client.set(key, value, ex=ttl)

    async def delete(self, key: str) -> None:
        """Delete a value from the cache.
        
        Args:
            key: The key to delete.
        """
        await self.client.delete(key) 