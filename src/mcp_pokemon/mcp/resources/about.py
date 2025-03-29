"""About resources for MCP server."""

from mcp.server.fastmcp import FastMCP


def register_about_resources(mcp: FastMCP) -> None:
    """Register about-related resources in the MCP server.
    
    Args:
        mcp: The MCP server instance.
    """
    
    @mcp.resource("about://author")
    def author_resource() -> str:
        """Return information about the author of this MCP server.
        
        Returns:
            Author information.
        """
        return "Daniel Yoshizawa" 