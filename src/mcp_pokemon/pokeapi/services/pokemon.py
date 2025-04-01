"""Pokemon service implementation."""

from typing import List, Dict, Any

from mcp_pokemon.pokeapi.models import Pokemon, EvolutionDetail, ChainLink, PokemonForm, PokemonHabitat
from mcp_pokemon.pokeapi.repositories.interfaces import PokemonRepository


class PokemonService:
    """Service for Pokemon operations."""

    def __init__(self, repository: PokemonRepository) -> None:
        """Initialize the service.

        Args:
            repository: The repository to use for data access.
        """
        self.repository = repository

    async def get_pokemon(self, identifier: str | int) -> Dict[str, Any]:
        """Get a Pokemon by name or ID.

        Args:
            identifier: The Pokemon name or ID.

        Returns:
            The Pokemon data as a dictionary.
        """
        pokemon = await self.repository.get_pokemon(identifier)
        return pokemon.model_dump()

    async def list_pokemon(self, offset: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        """List Pokemon with pagination.

        Args:
            offset: The offset for pagination.
            limit: The limit for pagination.

        Returns:
            List of Pokemon data as dictionaries.
        """
        response = await self.repository.list_pokemon(offset=offset, limit=limit)
        pokemon_list = []
        for resource in response.results:
            pokemon = await self.repository.get_pokemon(resource.name)
            pokemon_list.append(pokemon.model_dump())
        return pokemon_list

    def _format_evolution_details(self, details: EvolutionDetail) -> str:
        """Format evolution details into a human-readable string.

        Args:
            details: The evolution details to format.

        Returns:
            A human-readable string describing the evolution conditions.
        """
        conditions = []

        if details.min_level:
            conditions.append(f"reaching level {details.min_level}")
        if details.min_happiness:
            conditions.append(f"happiness of at least {details.min_happiness}")
        if details.min_affection:
            conditions.append(f"affection of at least {details.min_affection}")
        if details.item:
            conditions.append(f"using {details.item.name}")
        if details.held_item:
            conditions.append(f"holding {details.held_item.name}")
        if details.known_move:
            conditions.append(f"knowing the move {details.known_move.name}")
        if details.known_move_type:
            conditions.append(f"knowing a {details.known_move_type.name}-type move")
        if details.location:
            conditions.append(f"at {details.location.name}")
        if details.needs_overworld_rain:
            conditions.append("while it's raining")
        if details.party_species:
            conditions.append(f"with a {details.party_species.name} in the party")
        if details.party_type:
            conditions.append(f"with a {details.party_type.name}-type Pokemon in the party")
        if details.trade_species:
            conditions.append(f"by trading with {details.trade_species.name}")
        if details.time_of_day:
            conditions.append(f"during {details.time_of_day}")
        if details.relative_physical_stats is not None:
            if details.relative_physical_stats > 0:
                conditions.append("when Attack > Defense")
            elif details.relative_physical_stats < 0:
                conditions.append("when Attack < Defense")
            else:
                conditions.append("when Attack = Defense")
        if details.trigger.name == "trade" and not conditions:
            conditions.append("by trading")
        if not conditions and details.trigger.name == "level-up":
            conditions.append("by leveling up")

        return " ".join(conditions)

    def _format_evolution_chain(self, chain: ChainLink, indent: int = 0) -> List[str]:
        """Format an evolution chain into a list of strings.

        Args:
            chain: The evolution chain link to format.
            indent: The current indentation level.

        Returns:
            A list of strings describing the evolution chain.
        """
        result = []
        prefix = "    " * indent
        result.append(f"{prefix}{chain.species.name.title()}")

        for evolution in chain.evolves_to:
            if evolution.evolution_details:
                conditions = self._format_evolution_details(evolution.evolution_details[0])
                result.append(f"{prefix}└─> {evolution.species.name.title()} ({conditions})")
            else:
                result.append(f"{prefix}└─> {evolution.species.name.title()}")
            
            if evolution.evolves_to:
                result.extend(self._format_evolution_chain(evolution, indent + 1))

        return result

    async def get_evolution_chain(self, chain_id: int) -> str:
        """Get a formatted evolution chain by ID.

        Args:
            chain_id: The evolution chain ID.

        Returns:
            A formatted string showing the evolution chain.
        """
        chain = await self.repository.get_evolution_chain(chain_id)
        lines = self._format_evolution_chain(chain.chain)
        return "\n".join(lines)

    async def get_pokemon_evolution_chain(self, identifier: str | int) -> str:
        """Get the evolution chain for a specific Pokemon.

        Args:
            identifier: The Pokemon name or ID.

        Returns:
            A formatted string showing the Pokemon's evolution chain.
        """
        species = await self.repository.get_pokemon_species(identifier)
        chain_url = species.evolution_chain["url"]
        chain_id = int(chain_url.rstrip("/").split("/")[-1])
        return await self.get_evolution_chain(chain_id)

    async def get_pokemon_form_details(self, identifier: str | int) -> str:
        """Get detailed information about a Pokemon form.

        Args:
            identifier: The form name or ID.

        Returns:
            A formatted string with details about the Pokemon form.
        """
        form = await self.repository.get_pokemon_form(identifier)
        
        details = []
        details.append(f"Form: {form.name.title()}")
        if form.form_name:
            details.append(f"Form Name: {form.form_name}")
        
        # Add type information
        types = [t.type.name.title() for t in form.types]
        details.append(f"Types: {' / '.join(types)}")
        
        # Add form characteristics
        characteristics = []
        if form.is_mega:
            characteristics.append("Mega Evolution")
        if form.is_battle_only:
            characteristics.append("Battle-Only Form")
        if form.is_default:
            characteristics.append("Default Form")
        if characteristics:
            details.append(f"Characteristics: {', '.join(characteristics)}")
        
        # Add version group information
        details.append(f"Version Group: {form.version_group.name.replace('-', ' ').title()}")
        
        # Add sprite information if available
        available_sprites = [k for k, v in form.sprites.items() if v is not None]
        if available_sprites:
            details.append("Available Sprites: " + ", ".join(available_sprites))
        
        return "\n".join(details)

    async def get_pokemon_habitat_details(self, identifier: str | int) -> str:
        """Get detailed information about a Pokemon habitat.

        Args:
            identifier: The habitat name or ID.

        Returns:
            A formatted string with details about the Pokemon habitat.
        """
        habitat = await self.repository.get_pokemon_habitat(identifier)
        
        details = []
        # Add habitat name
        details.append(f"Habitat: {habitat.name.title()}")
        
        # Add localized names
        localized_names = [f"{name.name} ({name.language.name})" for name in habitat.names]
        if localized_names:
            details.append("Names in other languages:")
            details.extend(f"  - {name}" for name in localized_names)
        
        # Add Pokemon species that live in this habitat
        if habitat.pokemon_species:
            details.append(f"\nPokemon found in this habitat ({len(habitat.pokemon_species)}):")
            pokemon_list = sorted([species.name.title() for species in habitat.pokemon_species])
            details.extend(f"  - {pokemon}" for pokemon in pokemon_list)
        
        return "\n".join(details)

    async def compare_pokemon(self, pokemon1: str, pokemon2: str) -> str:
        """Compare two Pokemon and determine which would win in a battle.
        
        Args:
            pokemon1: Name or ID of the first Pokemon.
            pokemon2: Name or ID of the second Pokemon.
            
        Returns:
            A detailed comparison of the two Pokemon.
        """
        p1 = await self.repository.get_pokemon(pokemon1)
        p2 = await self.repository.get_pokemon(pokemon2)
        
        # Calculate total base stats
        p1_total = sum(stat.base_stat for stat in p1.stats)
        p2_total = sum(stat.base_stat for stat in p2.stats)

        # Get types and abilities
        p1_types = [t.type.name for t in p1.types]
        p2_types = [t.type.name for t in p2.types]
        p1_abilities = [a.ability.name for a in p1.abilities]
        p2_abilities = [a.ability.name for a in p2.abilities]

        # Build comparison text
        result = []
        result.append(f"Comparing {p1.name.title()} vs {p2.name.title()}:")
        
        result.append(f"\n{p1.name.title()}:")
        result.append(f"- Types: {', '.join(p1_types)}")
        result.append(f"- Abilities: {', '.join(p1_abilities)}")
        result.append(f"- Base Stats:")
        for stat in p1.stats:
            result.append(f"  * {stat.stat.name}: {stat.base_stat}")
        result.append(f"- Total base stats: {p1_total}")
        result.append(f"- Height: {p1.height/10}m")
        result.append(f"- Weight: {p1.weight/10}kg")
        
        result.append(f"\n{p2.name.title()}:")
        result.append(f"- Types: {', '.join(p2_types)}")
        result.append(f"- Abilities: {', '.join(p2_abilities)}")
        result.append(f"- Base Stats:")
        for stat in p2.stats:
            result.append(f"  * {stat.stat.name}: {stat.base_stat}")
        result.append(f"- Total base stats: {p2_total}")
        result.append(f"- Height: {p2.height/10}m")
        result.append(f"- Weight: {p2.weight/10}kg")

        # Determine winner based on stats and provide more detailed analysis
        result.append("\nBattle Analysis:")
        if p1_total > p2_total:
            diff = p1_total - p2_total
            result.append(f"{p1.name.title()} has an advantage with {diff} more total base stats!")
        elif p2_total > p1_total:
            diff = p2_total - p1_total
            result.append(f"{p2.name.title()} has an advantage with {diff} more total base stats!")
        else:
            result.append("Both Pokemon are evenly matched in total base stats!")

        return "\n".join(result) 