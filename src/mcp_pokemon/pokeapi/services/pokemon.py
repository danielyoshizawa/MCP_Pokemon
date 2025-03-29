"""Pokemon service implementation."""

from typing import List, Dict, Any

from mcp_pokemon.pokeapi.models import Pokemon
from mcp_pokemon.pokeapi.repositories.interfaces import PokemonRepository


class PokemonService:
    """Service for Pokemon operations."""

    def __init__(self, repository: PokemonRepository) -> None:
        """Initialize the service.

        Args:
            repository: The repository to use for data access.
        """
        self.repository = repository

    async def get_pokemon(self, identifier: str | int) -> Dict[str, Any]:
        """Get a Pokemon by name or ID.

        Args:
            identifier: The Pokemon name or ID.

        Returns:
            The Pokemon data as a dictionary.
        """
        pokemon = await self.repository.get_pokemon(identifier)
        return pokemon.model_dump()

    async def list_pokemon(self, offset: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        """List Pokemon with pagination.

        Args:
            offset: The offset for pagination.
            limit: The limit for pagination.

        Returns:
            List of Pokemon data as dictionaries.
        """
        response = await self.repository.list_pokemon(offset=offset, limit=limit)
        pokemon_list = []
        for resource in response.results:
            pokemon = await self.repository.get_pokemon(resource.name)
            pokemon_list.append(pokemon.model_dump())
        return pokemon_list

    async def compare_pokemon(self, pokemon1: str | int, pokemon2: str | int) -> str:
        """Compare two Pokemon and determine which would win in a battle.

        Args:
            pokemon1: Name or ID of the first Pokemon.
            pokemon2: Name or ID of the second Pokemon.

        Returns:
            A string describing the comparison result.
        """
        p1 = await self.repository.get_pokemon(pokemon1)
        p2 = await self.repository.get_pokemon(pokemon2)

        # Calculate total base stats
        p1_total = sum(stat.base_stat for stat in p1.stats)
        p2_total = sum(stat.base_stat for stat in p2.stats)

        # Get types
        p1_types = [t.type.name for t in p1.types]
        p2_types = [t.type.name for t in p2.types]

        return (
            f"Comparing {p1.name.title()} vs {p2.name.title()}:\n\n"
            f"{p1.name.title()}:\n"
            f"- Types: {', '.join(p1_types)}\n"
            f"- Total base stats: {p1_total}\n\n"
            f"{p2.name.title()}:\n"
            f"- Types: {', '.join(p2_types)}\n"
            f"- Total base stats: {p2_total}\n\n"
            f"{p1.name.title() if p1_total > p2_total else p2.name.title()} "
            f"would likely win with {max(p1_total, p2_total)} total base stats vs "
            f"{min(p1_total, p2_total)}!"
        ) 