"""Pokemon service implementation."""

from typing import List, Dict, Any, Optional, Tuple

from mcp_pokemon.pokeapi.models import Pokemon, EvolutionDetail, ChainLink, PokemonForm, PokemonHabitat, PokemonColor, PokemonShape, Type, Ability, Characteristic, Stat
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

    async def get_pokemon_color_details(self, identifier: str | int) -> str:
        """Get detailed information about a Pokemon color.

        Args:
            identifier: The color name or ID.

        Returns:
            A formatted string with details about the Pokemon color.
        """
        color = await self.repository.get_pokemon_color(identifier)
        
        details = []
        # Add color name
        details.append(f"Color: {color.name.title()}")
        
        # Add localized names
        localized_names = [f"{name.name} ({name.language.name})" for name in color.names]
        if localized_names:
            details.append("Names in other languages:")
            details.extend(f"  - {name}" for name in localized_names)
        
        # Add Pokemon species of this color
        if color.pokemon_species:
            details.append(f"\nPokemon of this color ({len(color.pokemon_species)}):")
            pokemon_list = sorted([species.name.title() for species in color.pokemon_species])
            # Group Pokemon in columns for better readability
            columns = 3
            for i in range(0, len(pokemon_list), columns):
                row = pokemon_list[i:i + columns]
                details.append("  " + "  ".join(f"{pokemon:<15}" for pokemon in row))
        
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

    async def get_pokemon_shape_details(self, identifier: str | int) -> str:
        """Get detailed information about a Pokemon shape.

        Args:
            identifier: The shape name or ID.

        Returns:
            A formatted string with details about the Pokemon shape.

        Raises:
            PokeAPINotFoundError: If the Pokemon shape is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        shape = await self.repository.get_pokemon_shape(identifier)

        # Format the shape name
        shape_name = shape.name.replace("-", " ").title()

        # Get names in other languages
        names_str = "Names in other languages:\n"
        for name in shape.names:
            names_str += f"  - {name.name} ({name.language.name})\n"

        # Get scientific names (awesome names)
        scientific_str = "Scientific names:\n"
        for name in shape.awesome_names:
            scientific_str += f"  - {name.awesome_name} ({name.language.name})\n"

        # Get Pokemon species with this shape
        pokemon_list = sorted([species.name.replace("-", " ").title() for species in shape.pokemon_species])
        
        # Format Pokemon list in columns
        max_name_length = max(len(name) for name in pokemon_list)
        column_width = max_name_length + 4
        num_columns = max(1, 80 // column_width)
        
        pokemon_str = f"\nPokemon of this shape ({len(pokemon_list)}):\n  "
        for i, name in enumerate(pokemon_list):
            if i > 0 and i % num_columns == 0:
                pokemon_str += "\n  "
            pokemon_str += f"{name:<{column_width}}"

        return f"Shape: {shape_name}\n\n{names_str}\n{scientific_str}{pokemon_str}"

    async def get_type_details(self, identifier: str | int) -> str:
        """Get detailed information about a Pokemon type.

        Args:
            identifier: The type name or ID.

        Returns:
            A formatted string with details about the Pokemon type.

        Raises:
            PokeAPINotFoundError: If the Pokemon type is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        type_data = await self.repository.get_type(identifier)

        # Format the type name
        type_name = type_data.name.replace("-", " ").title()

        # Get names in other languages
        names_str = "Names in other languages:\n"
        for name in type_data.names:
            names_str += f"  - {name.name} ({name.language.name})\n"

        # Format damage relations
        damage_relations = type_data.damage_relations
        
        relations_str = "\nDamage Relations:\n"
        
        # Super effective against (2x damage)
        relations_str += "\nSuper effective against:\n  "
        if damage_relations.double_damage_to:
            relations_str += ", ".join(t.name.title() for t in damage_relations.double_damage_to)
        else:
            relations_str += "None"

        # Not very effective against (0.5x damage)
        relations_str += "\n\nNot very effective against:\n  "
        if damage_relations.half_damage_to:
            relations_str += ", ".join(t.name.title() for t in damage_relations.half_damage_to)
        else:
            relations_str += "None"

        # No effect against (0x damage)
        relations_str += "\n\nNo effect against:\n  "
        if damage_relations.no_damage_to:
            relations_str += ", ".join(t.name.title() for t in damage_relations.no_damage_to)
        else:
            relations_str += "None"

        # Weak to (2x damage taken)
        relations_str += "\n\nWeak to:\n  "
        if damage_relations.double_damage_from:
            relations_str += ", ".join(t.name.title() for t in damage_relations.double_damage_from)
        else:
            relations_str += "None"

        # Resistant to (0.5x damage taken)
        relations_str += "\n\nResistant to:\n  "
        if damage_relations.half_damage_from:
            relations_str += ", ".join(t.name.title() for t in damage_relations.half_damage_from)
        else:
            relations_str += "None"

        # Immune to (0x damage taken)
        relations_str += "\n\nImmune to:\n  "
        if damage_relations.no_damage_from:
            relations_str += ", ".join(t.name.title() for t in damage_relations.no_damage_from)
        else:
            relations_str += "None"

        # Get Pokemon of this type
        pokemon_list = sorted([p.pokemon.name.replace("-", " ").title() for p in type_data.pokemon])
        
        # Format Pokemon list in columns
        max_name_length = max(len(name) for name in pokemon_list)
        column_width = max_name_length + 4
        num_columns = max(1, 80 // column_width)
        
        pokemon_str = f"\n\nPokemon of this type ({len(pokemon_list)}):\n  "
        for i, name in enumerate(pokemon_list):
            if i > 0 and i % num_columns == 0:
                pokemon_str += "\n  "
            pokemon_str += f"{name:<{column_width}}"

        return f"Type: {type_name}\n\n{names_str}{relations_str}{pokemon_str}"

    async def get_ability_details(self, identifier: str | int) -> str:
        """Get detailed information about a Pokemon ability.

        Args:
            identifier: The ability name or ID.

        Returns:
            A formatted string with details about the Pokemon ability.

        Raises:
            PokeAPINotFoundError: If the Pokemon ability is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        ability = await self.repository.get_ability(identifier)

        # Format ability name
        ability_name = ability.name.replace("-", " ").title()

        # Get names in other languages
        names = []
        for name in ability.names:
            names.append(f"  - {name.name} ({name.language.name})")

        # Get effect entries
        effects = []
        for effect in ability.effect_entries:
            if effect.language.name == "en":
                effects.append(effect.effect)

        # Get effect changes if any
        effect_changes = []
        for change in ability.effect_changes:
            for effect in change.effect_entries:
                if effect.language.name == "en":
                    effect_changes.append(f"  - {effect.effect} (from {change.version_group.name})")

        # Get Pokemon with this ability
        pokemon_list = []
        for pokemon in ability.pokemon:
            name = pokemon.pokemon.name.replace("-", " ").title()
            hidden = "(Hidden)" if pokemon.is_hidden else ""
            pokemon_list.append(f"{name} {hidden}")

        # Sort Pokemon list and format in columns
        pokemon_list.sort()
        max_length = max(len(name) for name in pokemon_list)
        columns = 2
        rows = (len(pokemon_list) + columns - 1) // columns
        pokemon_columns = []
        for i in range(rows):
            row = []
            for j in range(columns):
                idx = i + j * rows
                if idx < len(pokemon_list):
                    row.append(pokemon_list[idx].ljust(max_length + 2))
            pokemon_columns.append("  " + "".join(row))

        # Build the result string
        result = [
            f"Ability: {ability_name}",
            "",
            "Names in other languages:",
            *names,
            "",
            "Effect:",
            *[f"  {effect}" for effect in effects],
        ]

        if effect_changes:
            result.extend([
                "",
                "Effect changes:",
                *effect_changes,
            ])

        result.extend([
            "",
            "Pokemon with this ability:",
            *pokemon_columns,
        ])

        return "\n".join(result)

    async def get_characteristic_details(self, id: int) -> str:
        """Get detailed information about a Pokemon characteristic.

        Args:
            id: The characteristic ID.

        Returns:
            A formatted string containing details about the characteristic.

        Raises:
            PokeAPINotFoundError: If the characteristic is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        characteristic = await self.repository.get_characteristic(id)

        # Get the English description
        english_description = next(
            (desc.description for desc in characteristic.descriptions if desc.language.name == "en"),
            "No English description available"
        )

        # Format descriptions in other languages
        other_languages = []
        for desc in characteristic.descriptions:
            if desc.language.name != "en":
                other_languages.append(f"  - {desc.description} ({desc.language.name})")

        # Format the result string
        result = [
            f"Characteristic ID: {characteristic.id}",
            f"Description: {english_description}",
            f"Highest Stat: {characteristic.highest_stat.name}",
            f"Gene Modulo: {characteristic.gene_modulo}",
            f"Possible Values: {', '.join(map(str, characteristic.possible_values))}",
            "\nDescriptions in other languages:"
        ]

        if other_languages:
            result.extend(other_languages)
        else:
            result.append("  No translations available")

        return "\n".join(result)

    async def get_stat_details(self, identifier: str | int) -> str:
        """Get detailed information about a Pokemon stat.

        Args:
            identifier: The stat name or ID.

        Returns:
            A formatted string containing details about the stat.

        Raises:
            PokeAPINotFoundError: If the stat is not found.
            PokeAPIConnectionError: If there is a connection error.
            PokeAPIResponseError: If the response contains an error.
        """
        stat = await self.repository.get_stat(identifier)

        # Get the English name
        english_name = next(
            (name.name for name in stat.names if name.language.name == "en"),
            stat.name.replace("-", " ").title()
        )

        # Format names in other languages
        other_names = []
        for name in stat.names:
            if name.language.name != "en":
                other_names.append(f"  - {name.name} ({name.language.name})")

        # Format moves that affect this stat
        increasing_moves = []
        decreasing_moves = []
        for move in stat.affecting_moves.increase:
            if "move" in move:
                increasing_moves.append(move["move"]["name"].replace("-", " ").title())
        for move in stat.affecting_moves.decrease:
            if "move" in move:
                decreasing_moves.append(move["move"]["name"].replace("-", " ").title())

        # Format natures that affect this stat
        increasing_natures = [nature.name.replace("-", " ").title() for nature in stat.affecting_natures.increase]
        decreasing_natures = [nature.name.replace("-", " ").title() for nature in stat.affecting_natures.decrease]

        # Format the result string
        result = [
            f"Stat: {english_name}",
            f"ID: {stat.id}",
            f"Game Index: {stat.game_index}",
            f"Battle Only: {'Yes' if stat.is_battle_only else 'No'}",
        ]

        if stat.move_damage_class:
            result.append(f"Move Damage Class: {stat.move_damage_class.name.replace('-', ' ').title()}")

        if other_names:
            result.extend(["", "Names in other languages:"])
            result.extend(other_names)

        if increasing_moves:
            result.extend(["", "Moves that increase this stat:"])
            result.extend(f"  - {move}" for move in sorted(increasing_moves))

        if decreasing_moves:
            result.extend(["", "Moves that decrease this stat:"])
            result.extend(f"  - {move}" for move in sorted(decreasing_moves))

        if increasing_natures:
            result.extend(["", "Natures that increase this stat:"])
            result.extend(f"  - {nature}" for nature in sorted(increasing_natures))

        if decreasing_natures:
            result.extend(["", "Natures that decrease this stat:"])
            result.extend(f"  - {nature}" for nature in sorted(decreasing_natures))

        if stat.characteristics:
            result.extend(["", "Associated characteristics:"])
            result.extend(f"  - Characteristic #{char.url.split('/')[-2]}" for char in stat.characteristics)

        return "\n".join(result) 