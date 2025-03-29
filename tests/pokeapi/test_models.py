"""Tests for the PokeAPI models."""

import pytest
from pydantic import ValidationError

from mcp_pokemon.pokeapi.models import (
    NamedAPIResource,
    PaginatedResponse,
    Pokemon,
    PokemonAbility,
    PokemonSprites,
    PokemonStat,
    PokemonType,
    VersionGameIndex,
)


def test_named_api_resource():
    """Test the NamedAPIResource model."""
    data = {"name": "test", "url": "https://example.com"}
    resource = NamedAPIResource.model_validate(data)
    assert resource.name == "test"
    assert resource.url == "https://example.com"

    with pytest.raises(ValidationError):
        NamedAPIResource.model_validate({"name": "test"})


def test_version_game_index():
    """Test the VersionGameIndex model."""
    data = {
        "game_index": 1,
        "version": {"name": "test", "url": "https://example.com"},
    }
    index = VersionGameIndex.model_validate(data)
    assert index.game_index == 1
    assert index.version.name == "test"
    assert index.version.url == "https://example.com"


def test_pokemon_sprites():
    """Test the PokemonSprites model."""
    data = {
        "front_default": "https://example.com/front.png",
        "front_shiny": "https://example.com/front_shiny.png",
        "back_default": None,
        "back_shiny": None,
    }
    sprites = PokemonSprites.model_validate(data)
    assert sprites.front_default == "https://example.com/front.png"
    assert sprites.front_shiny == "https://example.com/front_shiny.png"
    assert sprites.back_default is None
    assert sprites.back_shiny is None


def test_pokemon_type():
    """Test the PokemonType model."""
    data = {
        "slot": 1,
        "type": {"name": "fire", "url": "https://example.com/type/fire"},
    }
    pokemon_type = PokemonType.model_validate(data)
    assert pokemon_type.slot == 1
    assert pokemon_type.type.name == "fire"
    assert pokemon_type.type.url == "https://example.com/type/fire"


def test_pokemon_ability():
    """Test the PokemonAbility model."""
    data = {
        "is_hidden": True,
        "slot": 1,
        "ability": {"name": "blaze", "url": "https://example.com/ability/blaze"},
    }
    ability = PokemonAbility.model_validate(data)
    assert ability.is_hidden is True
    assert ability.slot == 1
    assert ability.ability.name == "blaze"
    assert ability.ability.url == "https://example.com/ability/blaze"


def test_pokemon_stat():
    """Test the PokemonStat model."""
    data = {
        "base_stat": 100,
        "effort": 2,
        "stat": {"name": "hp", "url": "https://example.com/stat/hp"},
    }
    stat = PokemonStat.model_validate(data)
    assert stat.base_stat == 100
    assert stat.effort == 2
    assert stat.stat.name == "hp"
    assert stat.stat.url == "https://example.com/stat/hp"


def test_pokemon():
    """Test the Pokemon model."""
    data = {
        "id": 1,
        "name": "bulbasaur",
        "base_experience": 64,
        "height": 7,
        "is_default": True,
        "order": 1,
        "weight": 69,
        "abilities": [
            {
                "is_hidden": False,
                "slot": 1,
                "ability": {"name": "overgrow", "url": "https://example.com/ability/overgrow"},
            }
        ],
        "game_indices": [
            {
                "game_index": 1,
                "version": {"name": "red", "url": "https://example.com/version/red"},
            }
        ],
        "sprites": {
            "front_default": "https://example.com/sprites/bulbasaur.png",
            "back_default": None,
        },
        "stats": [
            {
                "base_stat": 45,
                "effort": 0,
                "stat": {"name": "hp", "url": "https://example.com/stat/hp"},
            }
        ],
        "types": [
            {
                "slot": 1,
                "type": {"name": "grass", "url": "https://example.com/type/grass"},
            }
        ],
    }
    pokemon = Pokemon.model_validate(data)
    assert pokemon.id == 1
    assert pokemon.name == "bulbasaur"
    assert pokemon.base_experience == 64
    assert pokemon.height == 7
    assert pokemon.is_default is True
    assert pokemon.order == 1
    assert pokemon.weight == 69
    assert len(pokemon.abilities) == 1
    assert len(pokemon.game_indices) == 1
    assert pokemon.sprites.front_default == "https://example.com/sprites/bulbasaur.png"
    assert len(pokemon.stats) == 1
    assert len(pokemon.types) == 1


def test_paginated_response():
    """Test the PaginatedResponse model."""
    data = {
        "count": 2,
        "next": "https://example.com/next",
        "previous": None,
        "results": [
            {"name": "test1", "url": "https://example.com/1"},
            {"name": "test2", "url": "https://example.com/2"},
        ],
    }
    response = PaginatedResponse[NamedAPIResource].model_validate(data)
    assert response.count == 2
    assert response.next == "https://example.com/next"
    assert response.previous is None
    assert len(response.results) == 2
    assert response.results[0].name == "test1"
    assert response.results[1].name == "test2"
