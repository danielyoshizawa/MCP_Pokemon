"""Cache decorators for the PokeAPI."""

import json
import hashlib
from functools import wraps
from typing import Any, Callable, Optional, TypeVar
from pydantic import BaseModel

from mcp_pokemon.pokeapi.cache.base import CacheProvider

T = TypeVar("T")


def generate_cache_key(prefix: str, *args: Any, **kwargs: Any) -> str:
    """Generate a cache key from the function arguments.
    
    Args:
        prefix: The prefix for the cache key (usually the function name).
        *args: Positional arguments to include in the key.
        **kwargs: Keyword arguments to include in the key.
        
    Returns:
        A unique cache key for the arguments.
    """
    # Convert args and kwargs to a string representation
    key_parts = [prefix]
    if args:
        key_parts.append(str(args))
    if kwargs:
        # Sort kwargs to ensure consistent ordering
        sorted_kwargs = sorted(kwargs.items())
        key_parts.append(str(sorted_kwargs))
    
    # Join all parts and create a hash
    key_str = ":".join(key_parts)
    return f"pokeapi:{hashlib.sha256(key_str.encode()).hexdigest()}"


def serialize_value(value: Any) -> str:
    """Serialize a value to JSON string.
    
    Args:
        value: The value to serialize.
        
    Returns:
        The serialized value as a JSON string.
    """
    if isinstance(value, BaseModel):
        return json.dumps(value.model_dump())
    elif isinstance(value, list):
        return json.dumps([
            item.model_dump() if isinstance(item, BaseModel) else item
            for item in value
        ])
    return json.dumps(value)


def deserialize_value(value: str, return_type: type) -> Any:
    """Deserialize a JSON string to a value.
    
    Args:
        value: The JSON string to deserialize.
        return_type: The expected return type.
        
    Returns:
        The deserialized value.
    """
    data = json.loads(value)
    if issubclass(return_type, BaseModel):
        return return_type.model_validate(data)
    elif hasattr(return_type, "__origin__") and return_type.__origin__ is list:
        item_type = return_type.__args__[0]
        if issubclass(item_type, BaseModel):
            return [item_type.model_validate(item) for item in data]
    return data


def cached(
    ttl: Optional[int] = None,
    prefix: Optional[str] = None,
    key_generator: Optional[Callable[..., str]] = None,
):
    """Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds. If None, the cache will not expire.
        prefix: Prefix for the cache key. If None, uses the function name.
        key_generator: Optional function to generate cache keys. If None, uses default.
        
    Returns:
        A decorator function that handles caching.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(self, *args: Any, **kwargs: Any) -> T:
            # Get the cache provider from the instance
            if not hasattr(self, "cache"):
                raise AttributeError("Instance must have a cache attribute")
            
            cache: CacheProvider = self.cache
            
            # Generate cache key
            cache_prefix = prefix or func.__name__
            if key_generator:
                key = key_generator(cache_prefix, *args, **kwargs)
            else:
                key = generate_cache_key(cache_prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_value = await cache.get(key)
            if cached_value is not None:
                return_type = func.__annotations__.get("return")
                return deserialize_value(cached_value, return_type)
            
            # If not in cache, call function and cache result
            result = await func(self, *args, **kwargs)
            await cache.set(key, serialize_value(result), ttl=ttl)
            
            return result
        return wrapper
    return decorator 