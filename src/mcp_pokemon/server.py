"""MCP Server for Pokemon data."""

import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp_pokemon.mcp.resources import register_all_resources
from mcp_pokemon.mcp.tools import register_all_tools
from mcp_pokemon.pokeapi import HTTPClient, PokeAPIRepository, PokemonService

# Initialize MCP server
mcp = FastMCP("Pokemon")
app = mcp.sse_app()

# Initialize PokeAPI components
client = HTTPClient("https://pokeapi.co/api/v2")
client.connect()
repository = PokeAPIRepository(client)
pokemon_service = PokemonService(repository)

# Register all tools and resources
register_all_tools(mcp, pokemon_service)
register_all_resources(mcp)

if __name__ == "__main__":
    print("Starting MCP Server")
    try:
        uvicorn.run("mcp_pokemon.server:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("Keyboard Interrupted")
    except Exception as ex:
        print(f"An unexpected error happened: {ex}")
    finally:
        print("Closing MCP server")
        client.close()