"""Interactive test script for the PokeAPI client."""

import asyncio
import json
from pathlib import Path

from mcp_pokemon.pokeapi.client import PokeAPIClient


async def main():
    """Test the PokeAPI client with real API calls."""
    print("Testing PokeAPI client...")
    
    async with PokeAPIClient() as client:
        # Test listing Pokemon
        print("\nListing first 5 Pokemon:")
        response = await client.list_pokemon(limit=5)
        print(f"Total Pokemon count: {response.count}")
        for pokemon in response.results:
            print(f"- {pokemon.name} ({pokemon.url})")

        # Test getting a specific Pokemon
        print("\nGetting details for Pikachu:")
        pokemon = await client.get_pokemon("pikachu")
        print(f"Pokemon ID: {pokemon.id}")
        print(f"Name: {pokemon.name}")
        print(f"Height: {pokemon.height}")
        print(f"Weight: {pokemon.weight}")
        print("\nTypes:")
        for type_info in pokemon.types:
            print(f"- {type_info.type.name}")
        print("\nAbilities:")
        for ability in pokemon.abilities:
            print(f"- {ability.ability.name} ({'Hidden' if ability.is_hidden else 'Normal'})")
        print("\nBase Stats:")
        for stat in pokemon.stats:
            print(f"- {stat.stat.name}: {stat.base_stat}")

        # Test error handling with a non-existent Pokemon
        print("\nTrying to get a non-existent Pokemon:")
        try:
            await client.get_pokemon("not-a-real-pokemon")
        except Exception as e:
            print(f"Got expected error: {type(e).__name__} - {str(e)}")


if __name__ == "__main__":
    asyncio.run(main()) 