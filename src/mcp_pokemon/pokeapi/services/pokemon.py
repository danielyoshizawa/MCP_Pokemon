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

    async def compare_pokemon(self, pokemon1: str, pokemon2: str) -> str:
        """Compare two Pokemon and determine which would win in a battle.
        
        Args:
            pokemon1: Name or ID of the first Pokemon.
            pokemon2: Name or ID of the second Pokemon.
            
        Returns:
            A detailed comparison of the two Pokemon.
        """
        p1 = await self.repository.get_pokemon(pokemon1)
        p2 = await self.repository.get_pokemon(pokemon2)
        
        # Calculate total base stats
        p1_total = sum(stat.base_stat for stat in p1.stats)
        p2_total = sum(stat.base_stat for stat in p2.stats)

        # Get types and abilities
        p1_types = [t.type.name for t in p1.types]
        p2_types = [t.type.name for t in p2.types]
        p1_abilities = [a.ability.name for a in p1.abilities]
        p2_abilities = [a.ability.name for a in p2.abilities]

        # Build comparison text
        result = []
        result.append(f"Comparing {p1.name.title()} vs {p2.name.title()}:")
        
        result.append(f"\n{p1.name.title()}:")
        result.append(f"- Types: {', '.join(p1_types)}")
        result.append(f"- Abilities: {', '.join(p1_abilities)}")
        result.append(f"- Base Stats:")
        for stat in p1.stats:
            result.append(f"  * {stat.stat.name}: {stat.base_stat}")
        result.append(f"- Total base stats: {p1_total}")
        result.append(f"- Height: {p1.height/10}m")
        result.append(f"- Weight: {p1.weight/10}kg")
        
        result.append(f"\n{p2.name.title()}:")
        result.append(f"- Types: {', '.join(p2_types)}")
        result.append(f"- Abilities: {', '.join(p2_abilities)}")
        result.append(f"- Base Stats:")
        for stat in p2.stats:
            result.append(f"  * {stat.stat.name}: {stat.base_stat}")
        result.append(f"- Total base stats: {p2_total}")
        result.append(f"- Height: {p2.height/10}m")
        result.append(f"- Weight: {p2.weight/10}kg")

        # Determine winner based on stats and provide more detailed analysis
        result.append("\nBattle Analysis:")
        if p1_total > p2_total:
            diff = p1_total - p2_total
            result.append(f"{p1.name.title()} has an advantage with {diff} more total base stats!")
        elif p2_total > p1_total:
            diff = p2_total - p1_total
            result.append(f"{p2.name.title()} has an advantage with {diff} more total base stats!")
        else:
            result.append("Both Pokemon are evenly matched in total base stats!")

        return "\n".join(result) 