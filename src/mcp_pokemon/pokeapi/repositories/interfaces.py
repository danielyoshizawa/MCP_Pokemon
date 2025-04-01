"""Repository interfaces for the PokeAPI."""

from typing import Protocol

from mcp_pokemon.pokeapi.models import NamedAPIResource, PaginatedResponse, Pokemon, PokemonSpecies, EvolutionChain, PokemonForm, PokemonHabitat, PokemonColor


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

    async def get_pokemon_species(self, identifier: str | int) -> PokemonSpecies:
        """Get a Pokemon species by name or ID.

        Args:
            identifier: The Pokemon species name or ID.

        Returns:
            The Pokemon species data.

        Raises:
            PokeAPINotFoundError: If the Pokemon species is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        ...

    async def get_evolution_chain(self, chain_id: int) -> EvolutionChain:
        """Get a Pokemon evolution chain by ID.

        Args:
            chain_id: The evolution chain ID.

        Returns:
            The evolution chain data.

        Raises:
            PokeAPINotFoundError: If the evolution chain is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        ...

    async def get_pokemon_form(self, identifier: str | int) -> PokemonForm:
        """Get a Pokemon form by name or ID.

        Args:
            identifier: The form name or ID.

        Returns:
            The Pokemon form data.

        Raises:
            PokeAPINotFoundError: If the Pokemon form is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        ...

    async def get_pokemon_habitat(self, identifier: str | int) -> PokemonHabitat:
        """Get a Pokemon habitat by name or ID.

        Args:
            identifier: The habitat name or ID.

        Returns:
            The Pokemon habitat data.

        Raises:
            PokeAPINotFoundError: If the Pokemon habitat is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        ...

    async def get_pokemon_color(self, identifier: str | int) -> PokemonColor:
        """Get a Pokemon color by name or ID.

        Args:
            identifier: The color name or ID.

        Returns:
            The Pokemon color data.

        Raises:
            PokeAPINotFoundError: If the Pokemon color is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        ... 