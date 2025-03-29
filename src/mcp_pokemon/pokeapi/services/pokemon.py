"""Pokemon service implementation."""

from mcp_pokemon.pokeapi.models import Pokemon
from mcp_pokemon.pokeapi.repositories import PokemonRepository


class PokemonService:
    """Service for Pokemon operations."""

    def __init__(self, repository: PokemonRepository) -> None:
        """Initialize the service.

        Args:
            repository: The repository to use for data access.
        """
        self.repository = repository

    async def get_pokemon(self, identifier: str | int) -> Pokemon:
        """Get a Pokemon by name or ID.

        Args:
            identifier: The Pokemon name or ID.

        Returns:
            The Pokemon data.
        """
        return await self.repository.get_pokemon(identifier)

    async def list_pokemon(self, offset: int = 0, limit: int = 20) -> list[Pokemon]:
        """List Pokemon with pagination.

        Args:
            offset: The offset for pagination.
            limit: The limit for pagination.

        Returns:
            List of Pokemon.
        """
        response = await self.repository.list_pokemon(offset=offset, limit=limit)
        pokemon_list = []
        for resource in response.results:
            pokemon = await self.get_pokemon(resource.name)
            pokemon_list.append(pokemon)
        return pokemon_list

    async def compare_pokemon(self, pokemon1: str | int, pokemon2: str | int) -> str:
        """Compare two Pokemon and determine which would win in a battle.

        Args:
            pokemon1: Name or ID of the first Pokemon.
            pokemon2: Name or ID of the second Pokemon.

        Returns:
            A string describing the comparison result.
        """
        p1 = await self.get_pokemon(pokemon1)
        p2 = await self.get_pokemon(pokemon2)

        # Calculate total base stats
        p1_total = sum(stat.base_stat for stat in p1.stats)
        p2_total = sum(stat.base_stat for stat in p2.stats)

        # Get types
        p1_types = [t.type.name for t in p1.types]
        p2_types = [t.type.name for t in p2.types]

        # Build comparison text
        result = []
        result.append(f"Comparing {p1.name.title()} vs {p2.name.title()}:")
        result.append(f"\n{p1.name.title()}:")
        result.append(f"- Types: {', '.join(p1_types)}")
        result.append(f"- Total base stats: {p1_total}")
        result.append(f"\n{p2.name.title()}:")
        result.append(f"- Types: {', '.join(p2_types)}")
        result.append(f"- Total base stats: {p2_total}")

        # Determine winner based on stats
        if p1_total > p2_total:
            result.append(f"\n{p1.name.title()} would likely win with {p1_total} total base stats vs {p2_total}!")
        elif p2_total > p1_total:
            result.append(f"\n{p2.name.title()} would likely win with {p2_total} total base stats vs {p1_total}!")
        else:
            result.append(f"\nIt's a tie! Both Pokemon have {p1_total} total base stats.")

        return "\n".join(result) 