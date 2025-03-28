from fastapi import FastAPI, HTTPException, Query
from mcp.server.fastmcp import FastMCP

from mcp_pokemon.api.errors import (
    MCPPokemonError,
    NotFoundError,
    ValidationError,
    mcp_pokemon_error_handler,
    http_exception_handler
)

# Create FastAPI app
app = FastAPI(
    title="MCP Pokemon",
    description="A Pokemon-focused implementation of the Model Context Protocol (MCP)",
    version="0.1.0"
)

# Register error handlers
app.add_exception_handler(MCPPokemonError, mcp_pokemon_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# Create MCP server instance
mcp = FastMCP("MCP Pokemon")

# Mount MCP server to FastAPI app at /mcp path
app.mount("/mcp", mcp.sse_app())

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mcp-pokemon"}

# Example endpoints demonstrating error handling
@app.get("/pokemon/{pokemon_id}")
async def get_pokemon(pokemon_id: int):
    """Example endpoint demonstrating NotFoundError"""
    if pokemon_id <= 0:
        raise ValidationError(
            message="Pokemon ID must be positive",
            details={"pokemon_id": pokemon_id, "constraint": "positive_integer"}
        )
    
    # Simulating a not found scenario for IDs > 1000
    if pokemon_id > 1000:
        raise NotFoundError(
            message=f"Pokemon with ID {pokemon_id} not found",
            details={"pokemon_id": pokemon_id}
        )
    
    # Simulating a successful response
    return {"id": pokemon_id, "name": "Example Pokemon"}

@app.post("/pokemon/team")
async def create_team(
    team_name: str = Query(..., min_length=3),
    pokemon_ids: list[int] = Query(..., min_items=1, max_items=6)
):
    """Example endpoint demonstrating ValidationError with multiple validation rules"""
    invalid_ids = [pid for pid in pokemon_ids if pid <= 0]
    if invalid_ids:
        raise ValidationError(
            message="Invalid Pokemon IDs in team",
            details={
                "invalid_ids": invalid_ids,
                "constraint": "all_ids_must_be_positive"
            }
        )
    
    if len(set(pokemon_ids)) != len(pokemon_ids):
        raise ValidationError(
            message="Duplicate Pokemon in team",
            details={
                "pokemon_ids": pokemon_ids,
                "constraint": "unique_pokemon_only"
            }
        )
    
    return {
        "team_name": team_name,
        "pokemon_ids": pokemon_ids
    }

@app.get("/pokemon/{pokemon_id}/evolution")
async def get_pokemon_evolution(pokemon_id: int):
    """Example endpoint demonstrating internal server error handling"""
    if pokemon_id == 0:
        # Simulating an unexpected internal error
        raise MCPPokemonError(
            message="Failed to fetch evolution data",
            details={
                "pokemon_id": pokemon_id,
                "error_source": "evolution_service",
                "error_code": "INTERNAL_ERROR"
            }
        )
    return {"evolution_chain": [pokemon_id, pokemon_id + 1]}

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