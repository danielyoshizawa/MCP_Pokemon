"""Tools package for MCP Pokemon."""

from mcp.server.fastmcp import FastMCP
from mcp_pokemon.pokeapi import PokemonService
from mcp_pokemon.mcp.tools.pokemon import register_pokemon_tools


def register_all_tools(mcp: FastMCP, service: PokemonService) -> None:
    """Register all MCP tools.
    
    Args:
        mcp: The MCP server instance.
        service: The Pokemon service instance.
    """
    register_pokemon_tools(mcp, service)


__all__ = [
    "register_all_tools",
    "register_pokemon_tools",
] 