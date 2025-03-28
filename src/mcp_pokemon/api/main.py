from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from mcp_pokemon.api.errors import (
    MCPPokemonError,
    NotFoundError,
    ValidationError,
    mcp_pokemon_error_handler,
    http_exception_handler
)
from mcp_pokemon.api.logging import setup_logging, get_logger
from mcp_pokemon.api.middleware import RequestLoggingMiddleware

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MCP Pokemon",
    description="""
    A Pokemon-focused implementation of the Model Context Protocol (MCP).
    
    This API provides:
    - Health check endpoint for monitoring
    - Pokemon information endpoints
    - MCP server integration for real-time updates
    
    All endpoints are logged with structured JSON logging, including:
    - Request/response details
    - Performance metrics
    - Error tracking
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "MCP Pokemon Team",
        "url": "https://github.com/danielyoshizawa/MCP_Pokemon",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Add middleware
app.add_middleware(RequestLoggingMiddleware)

# Register error handlers
app.add_exception_handler(MCPPokemonError, mcp_pokemon_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# Create MCP server instance
mcp = FastMCP("MCP Pokemon")

# Mount MCP server to FastAPI app at /mcp path
app.mount("/mcp", mcp.sse_app())

# Response models
class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(
        description="Current health status of the service",
        example="healthy"
    )
    service: str = Field(
        description="Name of the service",
        example="mcp-pokemon"
    )

class PokemonResponse(BaseModel):
    """Pokemon details response model"""
    id: int = Field(
        description="The unique identifier of the Pokemon",
        example=25,
        gt=0
    )
    name: str = Field(
        description="The name of the Pokemon",
        example="Pikachu"
    )

class TeamResponse(BaseModel):
    """Pokemon team response model"""
    team_name: str = Field(
        description="Name of the Pokemon team",
        example="Elite Four"
    )
    pokemon_ids: list[int] = Field(
        description="List of Pokemon IDs in the team",
        example=[25, 6, 149, 130, 59, 131],
        min_items=1,
        max_items=6
    )

class EvolutionResponse(BaseModel):
    """Pokemon evolution chain response model"""
    evolution_chain: list[int] = Field(
        description="List of Pokemon IDs in the evolution chain",
        example=[172, 25, 26]
    )

# Health check endpoint
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Service health check",
    description="Returns the current health status of the service",
    response_description="Health status information"
)
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"status": "healthy", "service": "mcp-pokemon"}

# Example endpoints demonstrating error handling
@app.get(
    "/pokemon/{pokemon_id}",
    response_model=PokemonResponse,
    tags=["Pokemon"],
    summary="Get Pokemon details",
    description="""
    Retrieves details for a specific Pokemon by its ID.
    
    The Pokemon ID must be a positive integer.
    Returns a 404 error if the Pokemon is not found (ID > 1000).
    Returns a 422 error if the ID is not positive.
    """,
    responses={
        404: {
            "description": "Pokemon not found",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "type": "NotFoundError",
                            "message": "Pokemon with ID 1001 not found",
                            "details": {"pokemon_id": 1001}
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "type": "ValidationError",
                            "message": "Pokemon ID must be positive",
                            "details": {
                                "pokemon_id": 0,
                                "constraint": "positive_integer"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def get_pokemon(pokemon_id: int):
    """Example endpoint demonstrating NotFoundError"""
    logger.info(f"Getting Pokemon details", extra={"pokemon_id": pokemon_id})
    
    if pokemon_id <= 0:
        logger.warning(
            "Invalid Pokemon ID provided",
            extra={"pokemon_id": pokemon_id, "error": "non_positive_id"}
        )
        raise ValidationError(
            message="Pokemon ID must be positive",
            details={"pokemon_id": pokemon_id, "constraint": "positive_integer"}
        )
    
    # Simulating a not found scenario for IDs > 1000
    if pokemon_id > 1000:
        logger.warning(
            "Pokemon not found",
            extra={"pokemon_id": pokemon_id, "error": "not_found"}
        )
        raise NotFoundError(
            message=f"Pokemon with ID {pokemon_id} not found",
            details={"pokemon_id": pokemon_id}
        )
    
    # Simulating a successful response
    logger.info(
        "Pokemon details retrieved",
        extra={"pokemon_id": pokemon_id}
    )
    return {"id": pokemon_id, "name": "Example Pokemon"}

@app.post(
    "/pokemon/team",
    response_model=TeamResponse,
    tags=["Pokemon"],
    summary="Create a Pokemon team",
    description="""
    Creates a new Pokemon team with the given name and Pokemon IDs.
    
    Requirements:
    - Team name must be at least 3 characters long
    - Team must have between 1 and 6 Pokemon
    - All Pokemon IDs must be positive
    - No duplicate Pokemon allowed in the team
    """,
    responses={
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "type": "ValidationError",
                            "message": "Invalid Pokemon IDs in team",
                            "details": {
                                "invalid_ids": [0, -1],
                                "constraint": "all_ids_must_be_positive"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def create_team(
    team_name: str = Query(..., min_length=3),
    pokemon_ids: list[int] = Query(..., min_items=1, max_items=6)
):
    """Example endpoint demonstrating ValidationError with multiple validation rules"""
    logger.info(
        "Creating Pokemon team",
        extra={"team_name": team_name, "pokemon_ids": pokemon_ids}
    )
    
    invalid_ids = [pid for pid in pokemon_ids if pid <= 0]
    if invalid_ids:
        logger.warning(
            "Invalid Pokemon IDs in team",
            extra={
                "team_name": team_name,
                "invalid_ids": invalid_ids,
                "error": "invalid_pokemon_ids"
            }
        )
        raise ValidationError(
            message="Invalid Pokemon IDs in team",
            details={
                "invalid_ids": invalid_ids,
                "constraint": "all_ids_must_be_positive"
            }
        )
    
    if len(set(pokemon_ids)) != len(pokemon_ids):
        logger.warning(
            "Duplicate Pokemon in team",
            extra={
                "team_name": team_name,
                "pokemon_ids": pokemon_ids,
                "error": "duplicate_pokemon"
            }
        )
        raise ValidationError(
            message="Duplicate Pokemon in team",
            details={
                "pokemon_ids": pokemon_ids,
                "constraint": "unique_pokemon_only"
            }
        )
    
    logger.info(
        "Team created successfully",
        extra={"team_name": team_name, "pokemon_ids": pokemon_ids}
    )
    return {
        "team_name": team_name,
        "pokemon_ids": pokemon_ids
    }

@app.get(
    "/pokemon/{pokemon_id}/evolution",
    response_model=EvolutionResponse,
    tags=["Pokemon"],
    summary="Get Pokemon evolution chain",
    description="""
    Retrieves the evolution chain for a specific Pokemon.
    
    This endpoint demonstrates internal error handling.
    For demonstration purposes, it will return an error for Pokemon ID 0.
    """,
    responses={
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "type": "MCPPokemonError",
                            "message": "Failed to fetch evolution data",
                            "details": {
                                "pokemon_id": 0,
                                "error_source": "evolution_service",
                                "error_code": "INTERNAL_ERROR"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def get_pokemon_evolution(pokemon_id: int):
    """Example endpoint demonstrating internal server error handling"""
    logger.info(
        "Getting Pokemon evolution chain",
        extra={"pokemon_id": pokemon_id}
    )
    
    if pokemon_id == 0:
        logger.error(
            "Evolution service error",
            extra={
                "pokemon_id": pokemon_id,
                "error": "evolution_service_error"
            }
        )
        # Simulating an unexpected internal error
        raise MCPPokemonError(
            message="Failed to fetch evolution data",
            details={
                "pokemon_id": pokemon_id,
                "error_source": "evolution_service",
                "error_code": "INTERNAL_ERROR"
            }
        )
    
    logger.info(
        "Evolution chain retrieved",
        extra={
            "pokemon_id": pokemon_id,
            "evolution_chain": [pokemon_id, pokemon_id + 1]
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