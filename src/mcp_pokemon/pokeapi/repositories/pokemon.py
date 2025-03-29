"""Repository implementation for Pokemon data access."""

from mcp_pokemon.pokeapi.cache import CacheProvider, cached
from mcp_pokemon.pokeapi.client import HTTPClient
from mcp_pokemon.pokeapi.models import NamedAPIResource, PaginatedResponse, Pokemon
from mcp_pokemon.pokeapi.repositories.interfaces import PokemonRepository


class PokeAPIRepository(PokemonRepository):
    """Repository for accessing Pokemon data from the PokeAPI."""

    def __init__(self, client: HTTPClient, cache: CacheProvider) -> None:
        """Initialize the repository.
        
        Args:
            client: The HTTP client to use.
            cache: The cache provider to use.
        """
        self.client = client
        self.cache = cache

    @cached(ttl=86400)  # Cache for 24 hours
    async def get_pokemon(self, identifier: str | int) -> Pokemon:
        """Get a Pokemon by name or ID.

        Args:
            identifier: The name or ID of the Pokemon.

        Returns:
            The Pokemon data.

        Raises:
            PokeAPINotFoundError: If the Pokemon is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        data = await self.client._get(f"/pokemon/{identifier}")
        # Ensure required fields are present for validation
        if isinstance(data, dict):
            data.setdefault("base_experience", 0)
            data.setdefault("height", 0)
            data.setdefault("weight", 0)
            data.setdefault("is_default", True)
            data.setdefault("order", 0)
            data.setdefault("sprites", {})
            data.setdefault("stats", [])
            data.setdefault("types", [])
            data.setdefault("abilities", [])
            data.setdefault("game_indices", [])
        return Pokemon.model_validate(data)

    @cached(ttl=86400)  # Cache for 24 hours
    async def list_pokemon(
        self, offset: int = 0, limit: int = 20
    ) -> PaginatedResponse[NamedAPIResource]:
        """List Pokemon with pagination.

        Args:
            offset: The offset for pagination.
            limit: The limit for pagination.

        Returns:
            A paginated response containing Pokemon resources.

        Raises:
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        data = await self.client._get("/pokemon", params={"offset": offset, "limit": limit})
        return PaginatedResponse[NamedAPIResource].model_validate(data) 