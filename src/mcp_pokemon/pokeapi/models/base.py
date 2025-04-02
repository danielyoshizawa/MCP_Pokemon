"""Base models for the PokeAPI."""
from typing import Generic, TypeVar, List, Optional, Dict, Any
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class NamedAPIResource(BaseModel):
    """A named resource in the PokeAPI."""

    name: str
    url: str

class APIResource(BaseModel):
    """A resource in the PokeAPI."""
    url: str

class Description(BaseModel):
    """A description in the PokeAPI."""
    description: str
    language: NamedAPIResource

class Effect(BaseModel):
    """An effect in the PokeAPI."""
    effect: str
    language: NamedAPIResource

class FlavorText(BaseModel):
    """A flavor text entry in the PokeAPI."""
    flavor_text: str
    language: NamedAPIResource
    version: Optional[NamedAPIResource] = None

class GenerationGameIndex(BaseModel):
    """A generation game index in the PokeAPI."""
    game_index: int
    generation: NamedAPIResource

class Name(BaseModel):
    """A name in the PokeAPI."""
    name: str
    language: NamedAPIResource

class VerboseEffect(BaseModel):
    """A verbose effect in the PokeAPI."""
    effect: str
    short_effect: str
    language: NamedAPIResource

class VersionGameIndex(BaseModel):
    """A version game index in the PokeAPI."""
    game_index: int
    version: NamedAPIResource

class PaginatedResponse(BaseModel, Generic[T]):
    """A paginated response from the PokeAPI."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[T]