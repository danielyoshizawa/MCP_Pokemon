"""Pokemon models for the PokeAPI."""
from typing import List, Optional
from pydantic import BaseModel, Field
from mcp_pokemon.pokeapi.models.base import NamedAPIResource, PaginatedResponse

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
    other: Optional[dict] = None
    versions: Optional[dict] = None


class PokemonType(BaseModel):
    """Represents a Pokémon type slot."""

    slot: int
    type: NamedAPIResource


class PokemonAbility(BaseModel):
    """Represents a Pokémon ability slot."""

    is_hidden: bool
    slot: int
    ability: NamedAPIResource


class PokemonFormType(BaseModel):
    """Type for a specific pokemon form."""

    slot: int
    type: NamedAPIResource


class PokemonTypePast(BaseModel):
    """Past type data for a pokemon."""

    generation: NamedAPIResource
    types: List[PokemonType]


class PokemonHeldItemVersion(BaseModel):
    """Version details for a held item."""

    version: NamedAPIResource
    rarity: int


class PokemonHeldItem(BaseModel):
    """An item a pokemon can hold."""

    item: NamedAPIResource
    version_details: List[PokemonHeldItemVersion]


class PokemonMoveVersion(BaseModel):
    """Version details for a move."""

    move_learn_method: NamedAPIResource
    version_group: NamedAPIResource
    level_learned_at: int


class PokemonMove(BaseModel):
    """A move the pokemon can learn."""

    move: NamedAPIResource
    version_group_details: List[PokemonMoveVersion]


class PokemonStat(BaseModel):
    """A pokemon's stats."""

    stat: NamedAPIResource
    effort: int
    base_stat: int


class Pokemon(BaseModel):
    """A Pokemon from the PokeAPI."""

    id: int
    name: str
    base_experience: int
    height: int
    is_default: bool
    order: int
    weight: int
    abilities: List[PokemonAbility]
    forms: List[NamedAPIResource]
    game_indices: List[dict]  # Using dict as it's a complex nested structure we don't need fully
    held_items: List[PokemonHeldItem]
    location_area_encounters: str
    moves: List[PokemonMove]
    past_types: List[PokemonTypePast]
    sprites: PokemonSprites
    species: NamedAPIResource
    stats: List[PokemonStat]
    types: List[PokemonType]


class PokemonList(PaginatedResponse[NamedAPIResource]):
    """A paginated list of Pokemon from the PokeAPI."""
    pass

class Name(BaseModel):
    """A name entry with language information."""
    
    name: str
    language: NamedAPIResource

class PalParkEncounter(BaseModel):
    """A Pal Park encounter entry."""
    
    area: NamedAPIResource
    base_score: int
    rate: int

class PokedexNumber(BaseModel):
    """A Pokedex number entry."""
    
    entry_number: int
    pokedex: NamedAPIResource

class FlavorText(BaseModel):
    """A flavor text entry for a Pokemon species."""
    
    flavor_text: str
    language: NamedAPIResource
    version: NamedAPIResource

class Genus(BaseModel):
    """A genus entry for a Pokemon species."""
    
    genus: str
    language: NamedAPIResource

class PokemonSpeciesVariety(BaseModel):
    """A variety of a Pokemon species."""
    
    is_default: bool
    pokemon: NamedAPIResource

class PokemonSpecies(BaseModel):
    """A Pokemon species from the PokeAPI."""
    
    id: int
    name: str
    order: int
    gender_rate: int = Field(description="The chance of this Pokémon being female, -1 for genderless")
    capture_rate: int
    base_happiness: int
    is_baby: bool
    is_legendary: bool
    is_mythical: bool
    hatch_counter: int
    has_gender_differences: bool
    forms_switchable: bool
    growth_rate: NamedAPIResource
    pokedex_numbers: List[PokedexNumber]
    egg_groups: List[NamedAPIResource]
    color: NamedAPIResource
    shape: Optional[NamedAPIResource] = None
    evolves_from_species: Optional[NamedAPIResource] = None
    evolution_chain: NamedAPIResource
    habitat: Optional[NamedAPIResource] = None
    generation: NamedAPIResource
    names: List[Name]
    pal_park_encounters: List[PalParkEncounter] = Field(alias="pal_park_encounters")
    flavor_text_entries: List[FlavorText] = Field(alias="flavor_text_entries")
    form_descriptions: List[dict] = Field(alias="form_descriptions")
    genera: List[Genus]
    varieties: List[PokemonSpeciesVariety]