from fastapi import status
import pytest
from fastapi.testclient import TestClient

from mcp_pokemon.api.main import app

client = TestClient(app)

def test_get_pokemon_success():
    """Test successful Pokemon retrieval"""
    response = client.get("/pokemon/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "name": "Example Pokemon"}

def test_get_pokemon_validation_error():
    """Test validation error for invalid Pokemon ID"""
    response = client.get("/pokemon/-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "error": {
            "type": "ValidationError",
            "message": "Pokemon ID must be positive",
            "details": {"pokemon_id": -1, "constraint": "positive_integer"}
        }
    }

def test_get_pokemon_not_found():
    """Test not found error for non-existent Pokemon"""
    response = client.get("/pokemon/1001")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "error": {
            "type": "NotFoundError",
            "message": "Pokemon with ID 1001 not found",
            "details": {"pokemon_id": 1001}
        }
    }

def test_create_team_success():
    """Test successful team creation"""
    response = client.post("/pokemon/team", params={
        "team_name": "Test Team",
        "pokemon_ids": [1, 2, 3]
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "team_name": "Test Team",
        "pokemon_ids": [1, 2, 3]
    }

def test_create_team_invalid_ids():
    """Test validation error for invalid Pokemon IDs in team"""
    response = client.post("/pokemon/team", params={
        "team_name": "Invalid Team",
        "pokemon_ids": [1, -1, 0]
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "error": {
            "type": "ValidationError",
            "message": "Invalid Pokemon IDs in team",
            "details": {
                "invalid_ids": [-1, 0],
                "constraint": "all_ids_must_be_positive"
            }
        }
    }

def test_create_team_duplicate_pokemon():
    """Test validation error for duplicate Pokemon in team"""
    response = client.post("/pokemon/team", params={
        "team_name": "Duplicate Team",
        "pokemon_ids": [1, 2, 2]
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "error": {
            "type": "ValidationError",
            "message": "Duplicate Pokemon in team",
            "details": {
                "pokemon_ids": [1, 2, 2],
                "constraint": "unique_pokemon_only"
            }
        }
    }

def test_get_evolution_success():
    """Test successful evolution chain retrieval"""
    response = client.get("/pokemon/1/evolution")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"evolution_chain": [1, 2]}

def test_get_evolution_internal_error():
    """Test internal server error in evolution endpoint"""
    response = client.get("/pokemon/0/evolution")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
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