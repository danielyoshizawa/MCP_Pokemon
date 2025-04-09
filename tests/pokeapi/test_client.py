"""Tests for the PokeAPI client."""

import pytest
import httpx
from unittest.mock import AsyncMock, patch

from mcp_pokemon.pokeapi.client import PokeAPIClient
from mcp_pokemon.pokeapi.client.exceptions import (
    PokeAPIConnectionError,
    PokeAPINotFoundError,
    PokeAPIRateLimitError,
    PokeAPIResponseError,
)
from mcp_pokemon.pokeapi.models import Pokemon, PaginatedResponse, NamedAPIResource


@pytest.fixture
def pokemon_data():
    """Sample Pokemon data for testing."""
    return {
        "id": 1,
        "name": "bulbasaur",
        "base_experience": 64,
        "height": 7,
        "weight": 69,
        "is_default": True,
        "order": 1, 
        "abilities": [
            {
                "ability": {
                    "name": "overgrow",
                    "url": "https://example.com/ability/overgrow",
                },
                "is_hidden": False,
                "slot": 1,
            }
        ],
        "game_indices": [
            {
                "game_index": 1,
                "version": {
                    "name": "red",
                    "url": "https://example.com/version/red",
                },
            }
        ],
        "sprites": {
            "front_default": "https://example.com/sprites/bulbasaur.png",
        },
        "stats": [
            {
                "base_stat": 45,
                "effort": 0,
                "stat": {
                    "name": "hp",
                    "url": "https://example.com/stat/hp",
                },
            }
        ],
        "types": [
            {
                "slot": 1,
                "type": {
                    "name": "grass",
                    "url": "https://example.com/type/grass",
                },
            }
        ],
    }


@pytest.fixture
def paginated_data():
    """Sample paginated data for testing."""
    return {
        "count": 2,
        "next": "https://example.com/next",
        "previous": None,
        "results": [
            {
                "name": "bulbasaur",
                "url": "https://example.com/pokemon/1",
            },
            {
                "name": "ivysaur",
                "url": "https://example.com/pokemon/2",
            },
        ],
    }


@pytest.mark.asyncio
async def test_client_lifecycle():
    """Test client lifecycle (connect, close)."""
    client = PokeAPIClient()
    assert client._client is None

    await client.connect()
    assert isinstance(client._client, httpx.AsyncClient)
    assert str(client._client.base_url).rstrip("/") == "https://pokeapi.co/api/v2"

    await client.close()
    assert client._client is None


@pytest.mark.asyncio
async def test_client_context_manager():
    """Test client as context manager."""
    async with PokeAPIClient() as client:
        assert isinstance(client._client, httpx.AsyncClient)
    assert client._client is None

@pytest.mark.asyncio
async def test_get_pokemon_success(pokemon_data):
    """Test getting a Pokemon successfully."""
    async with PokeAPIClient() as client:
        with patch.object(client._client, "get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json = lambda: pokemon_data
            mock_response.raise_for_status = lambda: None  # Método síncrono que não faz nada
            mock_get.return_value = mock_response

            pokemon = await client.get_pokemon("bulbasaur")
            assert isinstance(pokemon, Pokemon)
            assert pokemon.name == pokemon_data["name"]
            assert pokemon.id == pokemon_data["id"]

def raise_http_error(status_code: int, message: str, response: httpx.Response):
    """Helper function to raise HTTPStatusError."""
    raise httpx.HTTPStatusError(message, request=None, response=response)


@pytest.mark.asyncio
async def test_get_pokemon_not_found():
    """Test getting a non-existent Pokemon."""
    async with PokeAPIClient() as client:
        with patch.object(client._client, "get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status_code = 404
            mock_response.json = lambda: {"detail": "Not found"}
            
            def raise_404(*args, **kwargs):
                raise httpx.HTTPStatusError(
                    "404 Not Found",
                    request=None,
                    response=mock_response
                )
            
            mock_response.raise_for_status = raise_404
            mock_get.return_value = mock_response

            with pytest.raises(PokeAPINotFoundError):
                await client.get_pokemon("nonexistent")


@pytest.mark.asyncio
async def test_get_pokemon_rate_limit():
    """Test rate limit handling."""
    async with PokeAPIClient() as client:
        with patch.object(client._client, "get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status_code = 429
            mock_response.json = lambda: {"detail": "Rate limit exceeded"}
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "429 Too Many Requests",
                request=AsyncMock(),
                response=mock_response,
            )
            mock_get.return_value = mock_response

            with pytest.raises(PokeAPIRateLimitError):
                await client.get_pokemon("bulbasaur")


@pytest.mark.asyncio
async def test_get_pokemon_server_error():
    """Test server error handling."""
    async with PokeAPIClient() as client:
        with patch.object(client._client, "get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status_code = 500
            mock_response.json = lambda: {"detail": "Server error"}
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "500 Internal Server Error",
                request=AsyncMock(),
                response=mock_response,
            )
            mock_get.return_value = mock_response

            with pytest.raises(PokeAPIResponseError):
                await client.get_pokemon("bulbasaur")


@pytest.mark.asyncio
async def test_get_pokemon_connection_error():
    """Test connection error handling."""
    async with PokeAPIClient() as client:
        with patch.object(client._client, "get") as mock_get:
            mock_get.side_effect = httpx.RequestError("Connection failed")

            with pytest.raises(PokeAPIConnectionError) as exc_info:
                await client.get_pokemon("bulbasaur")
            assert "Connection error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_list_pokemon_success(paginated_data):
    """Test listing Pokemon successfully."""
    async with PokeAPIClient() as client:
        with patch.object(client._client, "get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json = lambda: paginated_data
            mock_get.return_value = mock_response

            response = await client.list_pokemon(offset=0, limit=2)
            assert isinstance(response, PaginatedResponse)
            assert response.count == paginated_data["count"]
            assert response.next == paginated_data["next"]
            assert response.previous == paginated_data["previous"]
            assert len(response.results) == len(paginated_data["results"])
