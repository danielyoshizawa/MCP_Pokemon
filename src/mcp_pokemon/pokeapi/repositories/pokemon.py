"""Pokemon repository implementation."""

from mcp_pokemon.pokeapi.client import HTTPClient
from mcp_pokemon.pokeapi.models import NamedAPIResource, PaginatedResponse, Pokemon
from mcp_pokemon.pokeapi.repositories.interfaces import PokemonRepository


class PokeAPIRepository(PokemonRepository):
    """Implementation of PokemonRepository using PokeAPI."""

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the repository.

        Args:
            client: The HTTP client to use for requests.
        """
        self.client = client

    def get_pokemon(self, identifier: str | int) -> Pokemon:
        """Get a Pokemon by name or ID.

        Args:
            identifier: The Pokemon name or ID.

        Returns:
            The Pokemon data.

        Raises:
            PokeAPINotFoundError: If the Pokemon is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        data = self.client._get(f"/pokemon/{identifier}")
        # Ensure required fields are present for validation
        if isinstance(data, dict):
            data.setdefault("base_experience", 0)
            data.setdefault("is_default", True)
            data.setdefault("order", 0)
            data.setdefault("sprites", {})
            data.setdefault("stats", [])
            data.setdefault("types", [])
            data.setdefault("abilities", [])
            data.setdefault("game_indices", [])
        return Pokemon.model_validate(data)

    def list_pokemon(
        self, offset: int = 0, limit: int = 20
    ) -> PaginatedResponse[NamedAPIResource]:
        """List Pokemon with pagination.

        Args:
            offset: The offset for pagination.
            limit: The limit for pagination.

        Returns:
            The paginated response containing Pokemon resources.

        Raises:
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        data = self.client._get("/pokemon", offset=offset, limit=limit)
        return PaginatedResponse[NamedAPIResource].model_validate(data) 