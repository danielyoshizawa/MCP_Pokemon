"""Resources package for MCP Pokemon."""

from mcp.server.fastmcp import FastMCP
from mcp_pokemon.mcp.resources.about import register_about_resources


def register_all_resources(mcp: FastMCP) -> None:
    """Register all MCP resources.
    
    Args:
        mcp: The MCP server instance.
    """
    register_about_resources(mcp)


__all__ = [
    "register_all_resources",
    "register_about_resources",
] 