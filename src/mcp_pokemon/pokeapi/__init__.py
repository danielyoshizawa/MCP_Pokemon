"""PokeAPI package."""

from mcp_pokemon.pokeapi.client import HTTPClient
from mcp_pokemon.pokeapi.client.exceptions import (
    PokeAPIConnectionError,
    PokeAPIError,
    PokeAPINotFoundError,
    PokeAPIRateLimitError,
    PokeAPIResponseError,
)
from mcp_pokemon.pokeapi.models import NamedAPIResource, PaginatedResponse, Pokemon
from mcp_pokemon.pokeapi.repositories import PokeAPIRepository, PokemonRepository
from mcp_pokemon.pokeapi.services import PokemonService

__all__ = [
    # Client
    "HTTPClient",
    # Exceptions
    "PokeAPIError",
    "PokeAPIConnectionError",
    "PokeAPIResponseError",
    "PokeAPINotFoundError",
    "PokeAPIRateLimitError",
    # Models
    "NamedAPIResource",
    "PaginatedResponse",
    "Pokemon",
    # Repository
    "PokemonRepository",
    "PokeAPIRepository",
    # Service
    "PokemonService",
]
