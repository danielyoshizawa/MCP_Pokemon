"""Repository interfaces for the PokeAPI."""

from typing import Protocol

from mcp_pokemon.pokeapi.models import NamedAPIResource, PaginatedResponse, Pokemon


class PokemonRepository(Protocol):
    """Interface for Pokemon data access."""

    async def get_pokemon(self, identifier: str | int) -> Pokemon:
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
        ...

    async def list_pokemon(
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
        ... 