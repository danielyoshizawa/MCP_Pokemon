import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

from mcp_pokemon.api.errors import (
    MCPPokemonError,
    NotFoundError,
    ValidationError,
    mcp_pokemon_error_handler,
    http_exception_handler
)

# Test app setup
@pytest.fixture
def app():
    app = FastAPI()
    app.add_exception_handler(MCPPokemonError, mcp_pokemon_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

# Test routes that raise different exceptions
def test_mcp_pokemon_error(app, client):
    @app.get("/test-base-error")
    async def raise_base_error():
        raise MCPPokemonError("Test base error", details={"test": "detail"})
    
    response = client.get("/test-base-error")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "error": {
            "type": "MCPPokemonError",
            "message": "Test base error",
            "details": {"test": "detail"}
        }
    }

def test_not_found_error(app, client):
    @app.get("/test-not-found")
    async def raise_not_found():
        raise NotFoundError("Resource not found", details={"resource_id": "123"})
    
    response = client.get("/test-not-found")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "error": {
            "type": "NotFoundError",
            "message": "Resource not found",
            "details": {"resource_id": "123"}
        }
    }

def test_validation_error(app, client):
    @app.get("/test-validation")
    async def raise_validation():
        raise ValidationError("Invalid input", details={"field": "name", "error": "required"})
    
    response = client.get("/test-validation")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "error": {
            "type": "ValidationError",
            "message": "Invalid input",
            "details": {"field": "name", "error": "required"}
        }
    }

def test_http_exception(app, client):
    @app.get("/test-http-error")
    async def raise_http_error():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    response = client.get("/test-http-error")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "error": {
            "type": "HTTPException",
            "message": "Not authorized",
            "details": {}
        }
    } 