"""Base interface for cache providers."""

from typing import Optional, Protocol


class CacheProvider(Protocol):
    """Protocol defining the interface for cache providers."""

    async def connect(self) -> None:
        """Connect to the cache server."""
        ...

    async def close(self) -> None:
        """Close the connection to the cache server."""
        ...

    async def get(self, key: str) -> Optional[str]:
        """Get a value from the cache.
        
        Args:
            key: The key to get the value for.
            
        Returns:
            The cached value if it exists, None otherwise.
        """
        ...

    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        """Set a value in the cache.
        
        Args:
            key: The key to set the value for.
            value: The value to cache.
            ttl: Time to live in seconds. If None, the value will not expire.
        """
        ...

    async def delete(self, key: str) -> None:
        """Delete a value from the cache.
        
        Args:
            key: The key to delete.
        """
        ... 