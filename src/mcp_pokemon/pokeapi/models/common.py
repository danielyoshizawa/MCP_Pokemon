"""Common models for the PokeAPI."""

from typing import Optional, List
from pydantic import BaseModel

from mcp_pokemon.pokeapi.models.base import NamedAPIResource


class Language(BaseModel):
    """A language that strings can be translated into."""
    id: int
    name: str
    official: bool
    iso639: str
    iso3166: str
    names: List[dict]


class VersionEncounterArea(BaseModel):
    """An area where a Pokemon can be encountered in a specific game version."""
    location_area: NamedAPIResource
    version_details: List[dict]


class VersionGroupFlavorText(BaseModel):
    """The flavor text for a specific version group."""
    text: str
    language: NamedAPIResource
    version_group: NamedAPIResource 