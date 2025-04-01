"""Pokemon models for the PokeAPI."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from mcp_pokemon.pokeapi.models.base import (
    APIResource,
    NamedAPIResource,
    PaginatedResponse,
    GenerationGameIndex,
    Effect,
    VerboseEffect,
    Description,
)

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

class PokemonColor(BaseModel):
    """A Pokemon color from the PokeAPI."""
    
    id: int
    name: str
    names: List[Name]
    pokemon_species: List[NamedAPIResource] = Field(alias="pokemon_species")

class AwesomeName(BaseModel):
    """Model for a Pokemon shape's awesome name in a specific language."""
    awesome_name: str
    language: NamedAPIResource

class PokemonShape(BaseModel):
    """Model for a Pokemon shape.
    
    A Pokemon shape represents the general physical structure of a Pokemon, such as 'ball', 'squiggle', etc.
    """
    id: int
    name: str
    awesome_names: List[AwesomeName]
    names: List[Name]
    pokemon_species: List[NamedAPIResource]

class TypeDamageRelations(BaseModel):
    """Model for type damage relations."""
    double_damage_from: List[NamedAPIResource]
    double_damage_to: List[NamedAPIResource]
    half_damage_from: List[NamedAPIResource]
    half_damage_to: List[NamedAPIResource]
    no_damage_from: List[NamedAPIResource]
    no_damage_to: List[NamedAPIResource]

class TypePastDamageRelations(BaseModel):
    """Model for past type damage relations."""
    damage_relations: TypeDamageRelations
    generation: NamedAPIResource

class TypePokemon(BaseModel):
    """Model for a Pokemon of a specific type."""
    pokemon: NamedAPIResource
    slot: int

class TypeSprites(BaseModel):
    """Model for type sprites."""
    generation_iii: Optional[Dict[str, Dict[str, str]]] = Field(alias="generation-iii")
    generation_iv: Optional[Dict[str, Dict[str, str]]] = Field(alias="generation-iv")
    generation_v: Optional[Dict[str, Dict[str, str]]] = Field(alias="generation-v")
    generation_vi: Optional[Dict[str, Dict[str, str]]] = Field(alias="generation-vi")
    generation_vii: Optional[Dict[str, Dict[str, str]]] = Field(alias="generation-vii")
    generation_viii: Optional[Dict[str, Dict[str, str]]] = Field(alias="generation-viii")
    generation_ix: Optional[Dict[str, Dict[str, str]]] = Field(alias="generation-ix")

class Type(BaseModel):
    """Model for a Pokemon type.
    
    A type is a property for Pokémon and their moves that defines their strengths and weaknesses.
    """
    id: int
    name: str
    damage_relations: TypeDamageRelations
    past_damage_relations: List[TypePastDamageRelations]
    game_indices: List[GenerationGameIndex]
    generation: NamedAPIResource
    move_damage_class: Optional[NamedAPIResource]
    names: List[Name]
    pokemon: List[TypePokemon]
    moves: List[NamedAPIResource]
    sprites: TypeSprites

class AbilityEffectChange(BaseModel):
    """Model for ability effect changes."""
    effect_entries: List[Effect]
    version_group: NamedAPIResource

class AbilityFlavorText(BaseModel):
    """Model for ability flavor text entries."""
    flavor_text: str
    language: NamedAPIResource
    version_group: NamedAPIResource

class AbilityPokemon(BaseModel):
    """Model for Pokemon that can have the ability."""
    is_hidden: bool
    pokemon: NamedAPIResource
    slot: int

class Ability(BaseModel):
    """Model for Pokemon abilities."""
    id: int
    name: str
    is_main_series: bool
    generation: NamedAPIResource
    names: List[Name]
    effect_entries: List[VerboseEffect]
    effect_changes: List[AbilityEffectChange]
    flavor_text_entries: List[AbilityFlavorText]
    pokemon: List[AbilityPokemon]

class Characteristic(BaseModel):
    """A Pokemon characteristic from the PokeAPI.
    
    Characteristics indicate which stat contains a Pokémon's highest IV.
    A characteristic is determined by the remainder of the highest IV divided by 5 (gene_modulo).
    """
    
    id: int
    gene_modulo: int
    possible_values: List[int]
    highest_stat: NamedAPIResource
    descriptions: List[Description]

class MoveStatAffectSets(BaseModel):
    """A set of moves that affect a stat."""
    
    increase: List[Dict[str, Any]] = Field(default_factory=list)
    decrease: List[Dict[str, Any]] = Field(default_factory=list)

class NatureStatAffectSets(BaseModel):
    """A set of natures that affect a stat."""
    
    increase: List[NamedAPIResource] = Field(default_factory=list)
    decrease: List[NamedAPIResource] = Field(default_factory=list)

class Stat(BaseModel):
    """A Pokemon stat from the PokeAPI."""
    
    id: int
    name: str
    game_index: int
    is_battle_only: bool
    affecting_moves: MoveStatAffectSets
    affecting_natures: NatureStatAffectSets
    characteristics: List[APIResource]
    move_damage_class: Optional[NamedAPIResource] = None
    names: List[Name]