# MCP_Pokemon

A Pokemon-focused implementation of the Model Context Protocol (MCP) for seamless integration between Pokemon data and Large Language Models (LLMs).

## About

This project implements the Model Context Protocol (MCP), an open protocol that enables seamless integration between LLM applications and external data sources. In this specific implementation, we focus on creating a bridge between Pokemon-related data and LLMs, allowing for rich interactions and data analysis in the Pokemon domain.

## Features

### Pokemon Data Access
- Basic Pokemon information retrieval
- Pokemon species details
- Evolution chain data
- Pokemon forms and variations
- Habitat information
- Color classification
- Shape categorization
- Type details and relationships
- Ability information
- Characteristic data
- Stats analysis
- Gender distribution
- Growth rate information
- Nature details
- Egg group categorization
- Location encounter data

### Technical Features
- Efficient caching with Redis
- Environment-based configuration
- Health check endpoint
- Structured logging
- Docker support for both development and production
- Clean architecture implementation (Repository Pattern)

## Technical Stack

- Python 3.11
- Model Context Protocol (MCP)
- Redis for caching
- Docker and Docker Compose
- Integration with PokeAPI
- Pydantic for data modeling

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11 (for local development)
- Redis (handled by Docker)

### Development Setup
1. Clone the repository:
```bash
git clone https://github.com/danielyoshizawa/MCP_Pokemon.git
cd MCP_Pokemon
```

2. Start the development environment:
```bash
docker compose up
```

The server will be available at `http://localhost:8000`

### Production Setup
1. Build the production image:
```bash
docker build -t mcp_pokemon:latest .
```

2. Run the container:
```bash
docker run -p 8000:8000 \
  -e REDIS_HOST=your-redis-host \
  -e REDIS_PORT=6379 \
  mcp_pokemon:latest
```

### Environment Variables
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `WORKERS` - Number of worker processes (default: 1)
- `LOG_LEVEL` - Logging level (default: info)
- `REDIS_HOST` - Redis host
- `REDIS_PORT` - Redis port (default: 6379)
- `REDIS_DB` - Redis database number (default: 0)
- `CACHE_TTL` - Cache time-to-live in seconds (default: 86400)
- `POKEAPI_URL` - PokeAPI base URL (default: https://pokeapi.co/api/v2)

## Available Tools

The following MCP tools are available:

- `get_pokemon` - Get detailed information about a specific Pokemon
- `list_pokemon` - List Pokemon with pagination
- `get_pokemon_species` - Get species information
- `get_evolution_chain` - Get evolution chain details
- `get_pokemon_form` - Get form information
- `get_pokemon_habitat` - Get habitat details
- `get_pokemon_color` - Get color information
- `get_pokemon_shape` - Get shape details
- `get_type` - Get type information
- `get_ability` - Get ability details
- `get_characteristic` - Get characteristic information
- `get_stat` - Get stat details
- `get_gender` - Get gender distribution
- `get_growth_rate` - Get growth rate information
- `get_nature` - Get nature details
- `get_egg_group` - Get egg group information
- `get_pokemon_encounters` - Get encounter locations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Model Context Protocol](https://github.com/modelcontextprotocol) - For the protocol specification
- [PokeAPI](https://pokeapi.co/) - For Pokemon data 