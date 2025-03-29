"""Pokemon tools for MCP server."""

from mcp.server.fastmcp import FastMCP
from mcp_pokemon.pokeapi import PokemonService


def register_pokemon_tools(mcp: FastMCP, service: PokemonService) -> None:
    """Register Pokemon-related tools in the MCP server.
    
    Args:
        mcp: The MCP server instance.
        service: The Pokemon service instance.
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
        result = await service.list_pokemon(offset=offset, limit=limit)
        return str([pokemon.name for pokemon in result])

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