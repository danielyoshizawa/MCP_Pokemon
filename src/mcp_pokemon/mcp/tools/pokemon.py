"""Pokemon tools for MCP."""

from mcp.server.fastmcp import FastMCP
from mcp_pokemon.pokeapi.services import PokemonService


def register_pokemon_tools(mcp: FastMCP, service: PokemonService) -> None:
    """Register Pokemon tools with MCP.
    
    Args:
        mcp: The MCP instance to register tools with.
        service: The Pokemon service to use.
    """
    
    @mcp.tool()
    async def list_pokemon(offset: int = 0, limit: int = 20) -> str:
        """List Pokemon with pagination.
        
        Args:
            offset: The offset for pagination.
            limit: The limit for pagination.
            
        Returns:
            A string representation of the paginated Pokemon list.
        """
        pokemon_list = await service.list_pokemon(offset=offset, limit=limit)
        return str([pokemon["name"] for pokemon in pokemon_list])

    @mcp.tool()
    async def compare_pokemon(pokemon1: str, pokemon2: str) -> str:
        """Compare two Pokemon and determine which would win in a battle.
        
        Args:
            pokemon1: Name or ID of the first Pokemon.
            pokemon2: Name or ID of the second Pokemon.
            
        Returns:
            A detailed comparison of the two Pokemon.
        """
        return await service.compare_pokemon(pokemon1, pokemon2) 