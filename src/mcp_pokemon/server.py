"""MCP Server for Pokemon data."""

import asyncio
import uvicorn
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP
from mcp_pokemon.mcp.resources import register_all_resources
from mcp_pokemon.mcp.tools import register_all_tools
from mcp_pokemon.pokeapi import HTTPClient, PokeAPIRepository, PokemonService

# Global variables for components that need to be shared
client = None
repository = None
pokemon_service = None
mcp = FastMCP("Pokemon")
app = mcp.sse_app()

@asynccontextmanager
async def lifespan(app):
    """Async context manager for FastAPI lifespan events."""
    # Startup
    print("Starting MCP Server")
    global client, repository, pokemon_service
    
    client = HTTPClient("https://pokeapi.co/api/v2")
    await client.connect()
    repository = PokeAPIRepository(client)
    pokemon_service = PokemonService(repository)
    
    # Register all tools and resources
    register_all_tools(mcp, pokemon_service)
    register_all_resources(mcp)
    
    yield
    
    # Shutdown
    print("Closing MCP server")
    if client:
        await client.close()

# Add lifespan event handler
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    try:
        uvicorn.run("mcp_pokemon.server:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("Keyboard Interrupted")
    except Exception as ex:
        print(f"An unexpected error happened: {ex}")