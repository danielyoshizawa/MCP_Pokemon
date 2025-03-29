"""Test configuration and fixtures."""

import pytest
from mcp_pokemon.pokeapi.client import PokeAPIClient

@pytest.fixture
async def pokeapi_client():
    """Fixture that provides a PokeAPI client."""
    async with PokeAPIClient() as client:
        yield client 