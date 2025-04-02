"""Repository implementation for Pokemon data access."""

from mcp_pokemon.pokeapi.cache import CacheProvider, cached
from mcp_pokemon.pokeapi.client import HTTPClient
from mcp_pokemon.pokeapi.models import (
    NamedAPIResource,
    PaginatedResponse,
    Pokemon,
    PokemonSpecies,
    EvolutionChain,
    PokemonForm,
    PokemonHabitat,
    PokemonColor,
    PokemonShape,
    Type,
    Ability,
    Characteristic,
    Stat,
    Gender,
)
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

    @cached(ttl=86400)  # Cache for 24 hours
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
        data = await self.client._get(f"/pokemon-species/{identifier}")
        return PokemonSpecies.model_validate(data)

    @cached(ttl=86400)  # Cache for 24 hours
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
        data = await self.client._get(f"/evolution-chain/{chain_id}")
        return EvolutionChain.model_validate(data)

    @cached(ttl=86400)  # Cache for 24 hours
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
        data = await self.client._get(f"/pokemon-form/{identifier}")
        return PokemonForm.model_validate(data)

    @cached(ttl=86400)  # Cache for 24 hours
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
        data = await self.client._get(f"/pokemon-habitat/{identifier}")
        return PokemonHabitat.model_validate(data)

    @cached(ttl=86400)  # Cache for 24 hours
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
        data = await self.client._get(f"/pokemon-color/{identifier}")
        return PokemonColor.model_validate(data)

    @cached(ttl=86400)  # Cache for 24 hours
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
        data = await self.client._get(f"/pokemon-shape/{identifier}")
        return PokemonShape.model_validate(data)

    @cached(ttl=86400)  # Cache for 24 hours
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
        data = await self.client._get(f"/type/{identifier}")
        return Type.model_validate(data)

    @cached(ttl=86400)  # Cache for 24 hours
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
        data = await self.client._get(f"/ability/{identifier}")
        return Ability.model_validate(data)

    @cached(ttl=86400)  # Cache for 24 hours
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
        data = await self.client._get(f"/characteristic/{id}")
        return Characteristic.model_validate(data)

    @cached(ttl=86400)  # Cache for 24 hours
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
        data = await self.client._get(f"/stat/{identifier}")
        return Stat.model_validate(data)

    @cached(ttl=86400)  # Cache for 24 hours
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
        data = await self.client._get(f"/gender/{identifier}")
        return Gender.model_validate(data) 