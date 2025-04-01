"""Pokemon models for the PokeAPI."""
from typing import List, Optional, Dict
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
    evolution_chain: Dict[str, str] = Field(description="URL to the evolution chain")
    habitat: Optional[NamedAPIResource] = None
    generation: NamedAPIResource
    names: List[Name]
    pal_park_encounters: List[PalParkEncounter] = Field(alias="pal_park_encounters")
    flavor_text_entries: List[FlavorText] = Field(alias="flavor_text_entries")
    form_descriptions: List[dict] = Field(alias="form_descriptions")
    genera: List[Genus]
    varieties: List[PokemonSpeciesVariety]


class EvolutionDetail(BaseModel):
    """Details about a Pokemon evolution."""
    
    item: Optional[NamedAPIResource] = None
    trigger: NamedAPIResource
    gender: Optional[int] = None
    held_item: Optional[NamedAPIResource] = None
    known_move: Optional[NamedAPIResource] = None
    known_move_type: Optional[NamedAPIResource] = None
    location: Optional[NamedAPIResource] = None
    min_level: Optional[int] = None
    min_happiness: Optional[int] = None
    min_beauty: Optional[int] = None
    min_affection: Optional[int] = None
    needs_overworld_rain: bool = False
    party_species: Optional[NamedAPIResource] = None
    party_type: Optional[NamedAPIResource] = None
    relative_physical_stats: Optional[int] = None
    time_of_day: str = ""
    trade_species: Optional[NamedAPIResource] = None
    turn_upside_down: bool = False


class ChainLink(BaseModel):
    """A link in the evolution chain."""
    
    is_baby: bool
    species: NamedAPIResource
    evolution_details: List[EvolutionDetail] = Field(default_factory=list)
    evolves_to: List["ChainLink"] = Field(default_factory=list)


class EvolutionChain(BaseModel):
    """A Pokemon evolution chain from the PokeAPI."""
    
    id: int
    baby_trigger_item: Optional[NamedAPIResource] = None
    chain: ChainLink

class PokemonForm(BaseModel):
    """A Pokemon form from the PokeAPI."""
    
    id: int
    name: str
    order: int
    form_order: int = Field(alias="form_order")
    is_default: bool = Field(alias="is_default")
    is_battle_only: bool = Field(alias="is_battle_only")
    is_mega: bool = Field(alias="is_mega")
    form_name: str = Field(alias="form_name")
    pokemon: NamedAPIResource
    sprites: Dict[str, Optional[str]]
    version_group: NamedAPIResource = Field(alias="version_group")
    types: List[PokemonType]
    form_names: List[Name] = Field(alias="form_names")
    names: List[Name]

class PokemonHabitat(BaseModel):
    """A Pokemon habitat from the PokeAPI."""
    
    id: int
    name: str
    names: List[Name]
    pokemon_species: List[NamedAPIResource] = Field(alias="pokemon_species")