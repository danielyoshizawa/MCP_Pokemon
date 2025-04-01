"""Pokemon tools for MCP."""

from mcp.server.fastmcp import FastMCP
from mcp_pokemon.pokeapi.services import PokemonService
from typing import List, Dict, Any


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
    async def get_pokemon(identifier: str) -> str:
        """Get detailed information about a specific Pokemon.
        
        Args:
            identifier: Name or ID of the Pokemon.
            
        Returns:
            A detailed description of the Pokemon.
        """
        pokemon = await service.get_pokemon(identifier)
        
        # Format the Pokemon information
        types = [t["type"]["name"] for t in pokemon["types"]]
        abilities = [a["ability"]["name"] for a in pokemon["abilities"]]
        stats = {s["stat"]["name"]: s["base_stat"] for s in pokemon["stats"]}
        total_stats = sum(stats.values())
        
        result = []
        result.append(f"Pokemon: {pokemon['name'].title()}")
        result.append(f"ID: {pokemon['id']}")
        result.append(f"Types: {', '.join(types)}")
        result.append(f"Abilities: {', '.join(abilities)}")
        result.append(f"Height: {pokemon['height']/10}m")
        result.append(f"Weight: {pokemon['weight']/10}kg")
        result.append("\nBase Stats:")
        for stat_name, base_stat in stats.items():
            result.append(f"- {stat_name}: {base_stat}")
        result.append(f"\nTotal Base Stats: {total_stats}")
        
        return "\n".join(result)

    @mcp.tool()
    async def get_evolution_chain(identifier: str) -> str:
        """Get the evolution chain for a specific Pokemon.
        
        Args:
            identifier: Name or ID of the Pokemon.
            
        Returns:
            A formatted string showing the Pokemon's evolution chain.
        """
        return await service.get_pokemon_evolution_chain(identifier)

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

    @mcp.tool()
    async def get_form(identifier: str) -> str:
        """Get detailed information about a specific Pokemon form.
        
        Args:
            identifier: Name or ID of the Pokemon form.
            
        Returns:
            A formatted string with details about the Pokemon form.
        """
        return await service.get_pokemon_form_details(identifier)

    @mcp.tool()
    async def get_habitat(identifier: str) -> str:
        """Get detailed information about a Pokemon habitat.
        
        Args:
            identifier: Name or ID of the habitat.
            
        Returns:
            A formatted string with details about the Pokemon habitat.
        """
        return await service.get_pokemon_habitat_details(identifier) 