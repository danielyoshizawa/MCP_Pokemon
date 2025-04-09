"""Redis cache implementation."""

from typing import Optional
import redis.asyncio as redis

from mcp_pokemon.pokeapi.cache.base import CacheProvider


class RedisCache(CacheProvider):
    """Redis implementation of the cache provider."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        username: Optional[str] = None,
        ssl: bool = False,
        redis_url: Optional[str] = None
    ) -> None:
        """Initialize the Redis cache.
        
        Args:
            host: Redis server host.
            port: Redis server port.
            db: Redis database number.
            password: Redis password.
            username: Redis username.
            ssl: Whether to use SSL.
            redis_url: Optional Redis URL (overrides other parameters if provided).
        """
        self.redis_url = redis_url
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.username = username
        self.ssl = ssl
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
            if self.redis_url:
                self._client = redis.from_url(
                    self.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
            else:
                self._client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    password=self.password,
                    username=self.username,
                    ssl=self.ssl,
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