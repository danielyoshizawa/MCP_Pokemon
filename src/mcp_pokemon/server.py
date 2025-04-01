"""MCP Server for Pokemon data."""

import asyncio
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

import uvicorn
from mcp.server.fastmcp import FastMCP

from mcp_pokemon.mcp.resources import register_all_resources
from mcp_pokemon.mcp.tools import register_all_tools
from mcp_pokemon.pokeapi import HTTPClient, PokeAPIRepository, PokemonService
from mcp_pokemon.pokeapi.cache import RedisCache

# Load environment variables
load_dotenv()

# Global variables for components that need to be shared
client = None
cache = None
repository = None
pokemon_service = None
mcp = FastMCP("Pokemon")
app = mcp.sse_app()

@asynccontextmanager
async def lifespan(app):
    """Async context manager for FastAPI lifespan events."""
    # Startup
    print("Starting MCP Server")
    global client, cache, repository, pokemon_service
    
    # Initialize components
    client = HTTPClient(os.getenv("POKEAPI_URL", "https://pokeapi.co/api/v2"))
    cache = RedisCache(os.getenv("REDIS_URL", "redis://localhost:6379"))
    
    # Connect to services
    await client.connect()
    await cache.connect()
    
    # Initialize repository and service
    repository = PokeAPIRepository(client, cache)
    pokemon_service = PokemonService(repository)
    
    # Register all tools and resources
    register_all_tools(mcp, pokemon_service)
    register_all_resources(mcp)
    
    yield
    
    # Shutdown
    print("Closing MCP server. Bye Pokeworld!")
    if client:
        await client.close()
    if cache:
        await cache.close()

# Add lifespan event handler
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    try:
        uvicorn.run(
            "mcp_pokemon.server:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )
    except KeyboardInterrupt:
        print("Keyboard Interrupted")
    except Exception as ex:
        print(f"An unexpected error happened: {ex}")