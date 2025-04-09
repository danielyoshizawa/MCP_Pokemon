"""Repositories package for PokeAPI."""

from mcp_pokemon.pokeapi.repositories.interfaces import PokemonRepository
from mcp_pokemon.pokeapi.repositories.pokemon import PokeAPIRepository

__all__ = [
    "PokemonRepository",  # Interface
    "PokeAPIRepository",  # Implementation
] 