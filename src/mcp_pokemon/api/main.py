from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

# Create FastAPI app
app = FastAPI(
    title="MCP Pokemon",
    description="A Pokemon-focused implementation of the Model Context Protocol (MCP)",
    version="0.1.0"
)

# Create MCP server instance
mcp = FastMCP("MCP Pokemon")

# Mount MCP server to FastAPI app at /mcp path
app.mount("/mcp", mcp.sse_app())

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mcp-pokemon"}

# Basic MCP resource example
@mcp.resource("status://health")
async def status_resource() -> str:
    """Provide the service status as a resource"""
    return "MCP Pokemon service is running"

# Basic MCP tool example
@mcp.tool()
async def get_service_info() -> dict:
    """Get basic service information"""
    return {
        "name": "MCP Pokemon",
        "version": "0.1.0",
        "status": "running",
        "description": "Pokemon data service using Model Context Protocol"
    }

# Basic MCP prompt example
@mcp.prompt()
async def help_prompt() -> str:
    """Create a help prompt for the service"""
    return """
    Welcome to the MCP Pokemon service!
    
    This service provides Pokemon information through the Model Context Protocol.
    You can:
    - Use resources to access Pokemon data
    - Use tools to query and analyze Pokemon information
    - Use prompts to get help and guidance
    
    How can I assist you with Pokemon information today?
    """ 