"""Pydantic models for the PokeAPI responses."""

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class NamedAPIResource(BaseModel):
    """A named resource in the PokeAPI."""

    name: str
    url: str


class VersionGameIndex(BaseModel):
    """A version game index in the PokeAPI."""

    game_index: int
    version: NamedAPIResource


class PokemonSprites(BaseModel):
    """Pokemon sprites from the PokeAPI."""

    front_default: Optional[str] = None
    front_shiny: Optional[str] = None
    front_female: Optional[str] = None
    front_shiny_female: Optional[str] = None
    back_default: Optional[str] = None
    back_shiny: Optional[str] = None
    back_female: Optional[str] = None
    back_shiny_female: Optional[str] = None


class PokemonType(BaseModel):
    """A Pokemon type from the PokeAPI."""

    slot: int
    type: NamedAPIResource


class PokemonAbility(BaseModel):
    """A Pokemon ability from the PokeAPI."""

    is_hidden: bool = Field(alias="is_hidden")
    slot: int
    ability: NamedAPIResource


class PokemonStat(BaseModel):
    """A Pokemon stat from the PokeAPI."""

    base_stat: int = Field(alias="base_stat")
    effort: int
    stat: NamedAPIResource


class Pokemon(BaseModel):
    """A Pokemon from the PokeAPI."""

    id: int
    name: str
    base_experience: int = Field(alias="base_experience")
    height: int
    is_default: bool = Field(alias="is_default")
    order: int
    weight: int
    abilities: List[PokemonAbility]
    game_indices: List[VersionGameIndex] = Field(alias="game_indices")
    sprites: PokemonSprites
    stats: List[PokemonStat]
    types: List[PokemonType]


class PaginatedResponse(BaseModel, Generic[T]):
    """A paginated response from the PokeAPI."""

    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[T]


class HTTPError(BaseModel):
    """HTTP error response model."""

    detail: str
