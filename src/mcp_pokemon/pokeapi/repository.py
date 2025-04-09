"""Repository for accessing the PokeAPI."""

from typing import List

from mcp_pokemon.pokeapi.client import HTTPClient
from mcp_pokemon.pokeapi.models import Pokemon, PokemonList


class PokeAPIRepository:
    """Repository for accessing the PokeAPI."""

    def __init__(self, client: HTTPClient) -> None:
        """Initialize the repository.
        
        Args:
            client: The HTTP client to use.
        """
        self._client = client

    async def get_pokemon(self, name_or_id: str) -> Pokemon:
        """Get a Pokemon by name or ID.
        
        Args:
            name_or_id: The name or ID of the Pokemon.
            
        Returns:
            The Pokemon data.
            
        Raises:
            PokeAPINotFoundError: If the Pokemon was not found.
            PokeAPIConnectionError: If there was an error connecting to the API.
            PokeAPIResponseError: If there was an error with the response.
        """
        data = await self._client._get(f"pokemon/{name_or_id.lower()}")
        return Pokemon.model_validate(data)

    async def list_pokemon(self, offset: int = 0, limit: int = 20) -> List[Pokemon]:
        """List Pokemon with pagination.
        
        Args:
            offset: The offset for pagination.
            limit: The limit for pagination.
            
        Returns:
            A list of Pokemon data.
            
        Raises:
            PokeAPIConnectionError: If there was an error connecting to the API.
            PokeAPIResponseError: If there was an error with the response.
        """
        data = await self._client._get("pokemon", params={"offset": offset, "limit": limit})
        pokemon_list = PokemonList.model_validate(data)
        return pokemon_list.results 