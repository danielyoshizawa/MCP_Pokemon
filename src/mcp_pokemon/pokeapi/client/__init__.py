"""Client package for PokeAPI."""

from mcp_pokemon.pokeapi.client.base import HTTPClient
from mcp_pokemon.pokeapi.client.exceptions import (
    PokeAPIError,
    PokeAPIConnectionError,
    PokeAPINotFoundError,
    PokeAPIRateLimitError,
    PokeAPIResponseError,
)

__all__ = [
    "HTTPClient",
    "PokeAPIError",
    "PokeAPIConnectionError",
    "PokeAPINotFoundError",
    "PokeAPIRateLimitError",
    "PokeAPIResponseError",
] 