"""MCP Server for Pokemon data."""

import asyncio
import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from dotenv import load_dotenv
import uvicorn
from mcp.server.fastmcp import FastMCP

from mcp_pokemon.mcp.resources import register_all_resources
from mcp_pokemon.mcp.tools import register_all_tools
from mcp_pokemon.pokeapi import HTTPClient, PokeAPIRepository, PokemonService
from mcp_pokemon.pokeapi.cache import RedisCache

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def get_settings() -> Dict[str, Any]:
    """Get application settings from environment variables."""
    return {
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": int(os.getenv("PORT", "8000")),
        "workers": int(os.getenv("WORKERS", "1")),
        "reload": os.getenv("ENVIRONMENT", "development").lower() == "development",
        "log_level": os.getenv("LOG_LEVEL", "info").lower(),
        "redis_host": os.getenv("REDIS_HOST", "localhost"),
        "redis_port": int(os.getenv("REDIS_PORT", "6379")),
        "redis_db": int(os.getenv("REDIS_DB", "0")),
        "cache_ttl": int(os.getenv("CACHE_TTL", "86400")),
        "pokeapi_url": os.getenv("POKEAPI_URL", "https://pokeapi.co/api/v2")
    }

async def wait_for_redis(cache: RedisCache, max_retries: int = 5, delay: int = 1) -> None:
    """Wait for Redis to become available.
    
    Args:
        cache: The Redis cache instance
        max_retries: Maximum number of connection attempts
        delay: Delay between attempts in seconds
    
    Raises:
        ConnectionError: If Redis is not available after max_retries
    """
    for attempt in range(max_retries):
        try:
            await cache.connect()
            logger.info("Successfully connected to Redis")
            return
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to connect to Redis after {max_retries} attempts")
                raise
            logger.warning(f"Failed to connect to Redis (attempt {attempt + 1}/{max_retries}): {e}")
            await asyncio.sleep(delay)

# Global variables for components that need to be shared
client = None
cache = None
repository = None
pokemon_service = None
mcp = FastMCP("Pokemon")
app = mcp.sse_app()

# Add health check endpoint
@app.route("/health")
async def health_check(request):
    """Health check endpoint."""
    return app.response_class(content={"status": "healthy"}, media_type="application/json")

@asynccontextmanager
async def lifespan(app):
    """Async context manager for FastAPI lifespan events."""
    # Startup
    logger.info("Starting MCP Server")
    global client, cache, repository, pokemon_service
    
    settings = get_settings()
    
    # Initialize components
    client = HTTPClient(settings["pokeapi_url"])
    cache = RedisCache(
        host=settings["redis_host"],
        port=settings["redis_port"],
        db=settings["redis_db"]
    )
    
    try:
        # Connect to services
        await client.connect()
        await wait_for_redis(cache)
        
        # Initialize repository and service
        repository = PokeAPIRepository(client, cache)
        pokemon_service = PokemonService(repository)
        
        # Register all tools and resources
        register_all_tools(mcp, pokemon_service)
        register_all_resources(mcp)
        
        logger.info("MCP Server started successfully")
        yield
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Closing MCP server. Bye Pokeworld!")
        if client:
            await client.close()
        if cache:
            await cache.close()

# Add lifespan event handler
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    try:
        settings = get_settings()
        uvicorn.run(
            "mcp_pokemon.server:app",
            host=settings["host"],
            port=settings["port"],
            reload=settings["reload"],
            workers=settings["workers"],
            log_level=settings["log_level"]
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")