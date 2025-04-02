"""Repository interfaces for the PokeAPI."""

from typing import Protocol
from abc import ABC, abstractmethod

from mcp_pokemon.pokeapi.models import NamedAPIResource, PaginatedResponse, Pokemon, PokemonSpecies, EvolutionChain, PokemonForm, PokemonHabitat, PokemonColor, PokemonShape, Type, Ability, Characteristic, Stat, Gender, GrowthRate


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

    async def get_pokemon_shape(self, identifier: str | int) -> PokemonShape:
        """Get a Pokemon shape by name or ID.
        
        Args:
            identifier: The shape name or ID.

        Returns:
            The Pokemon shape data.

        Raises:
            PokeAPINotFoundError: If the Pokemon shape is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        ...

    async def get_type(self, identifier: str | int) -> Type:
        """Get a Pokemon type by name or ID.
        
        Args:
            identifier: The type name or ID.

        Returns:
            The Pokemon type data.

        Raises:
            PokeAPINotFoundError: If the Pokemon type is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        ...

    async def get_ability(self, identifier: str | int) -> Ability:
        """Get a Pokemon ability by name or ID.

        Args:
            identifier: The ability name or ID.

        Returns:
            The Pokemon ability data.

        Raises:
            PokeAPINotFoundError: If the Pokemon ability is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        ...

    @abstractmethod
    async def get_characteristic(self, id: int) -> Characteristic:
        """Get a Pokemon characteristic by ID.

        Args:
            id: The characteristic ID.

        Returns:
            The Pokemon characteristic data.

        Raises:
            PokeAPINotFoundError: If the characteristic is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        pass

    @abstractmethod
    async def get_stat(self, identifier: str | int) -> Stat:
        """Get a Pokemon stat by name or ID.

        Args:
            identifier: The stat name or ID.

        Returns:
            The Pokemon stat data.

        Raises:
            PokeAPINotFoundError: If the stat is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        pass

    @abstractmethod
    async def get_gender(self, identifier: str | int) -> Gender:
        """Get a Pokemon gender by name or ID.

        Args:
            identifier: The gender name or ID.

        Returns:
            The Pokemon gender data.

        Raises:
            PokeAPINotFoundError: If the gender is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        pass

    @abstractmethod
    async def get_growth_rate(self, identifier: str | int) -> GrowthRate:
        """Get a Pokemon growth rate by name or ID.

        Args:
            identifier: The growth rate name or ID.

        Returns:
            The Pokemon growth rate data.

        Raises:
            PokeAPINotFoundError: If the growth rate is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        pass 