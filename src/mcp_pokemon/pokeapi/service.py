"""Service for accessing Pokemon data."""

from mcp_pokemon.pokeapi.models import Pokemon, NamedAPIResource
from mcp_pokemon.pokeapi.repository import PokeAPIRepository


class PokemonService:
    """Service for accessing Pokemon data."""

    def __init__(self, repository: PokeAPIRepository) -> None:
        """Initialize the service.
        
        Args:
            repository: The repository to use.
        """
        self._repository = repository

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
        return await self._repository.get_pokemon(name_or_id)

    async def list_pokemon(self, offset: int = 0, limit: int = 20) -> list[NamedAPIResource]:
        """List Pokemon with pagination.
        
        Args:
            offset: The offset for pagination.
            limit: The limit for pagination.
            
        Returns:
            A list of Pokemon resources.
            
        Raises:
            PokeAPIConnectionError: If there was an error connecting to the API.
            PokeAPIResponseError: If there was an error with the response.
        """
        response = await self._repository.list_pokemon(offset=offset, limit=limit)
        return response.results

    async def compare_pokemon(self, pokemon1: str, pokemon2: str) -> str:
        """Compare two Pokemon and determine which would win in a battle.
        
        Args:
            pokemon1: Name or ID of the first Pokemon.
            pokemon2: Name or ID of the second Pokemon.
            
        Returns:
            A detailed comparison of the two Pokemon.
            
        Raises:
            PokeAPINotFoundError: If either Pokemon was not found.
            PokeAPIConnectionError: If there was an error connecting to the API.
            PokeAPIResponseError: If there was an error with the response.
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