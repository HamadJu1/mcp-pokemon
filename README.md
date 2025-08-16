# MCP Pokémon

A minimal deterministic Pokémon battle simulator wrapped in an MCP server.

## Quick Start

These steps get a fresh checkout running on any machine:

```bash
# 1. Clone the repository
git clone https://github.com/your-org/mcp-pokemon.git
cd mcp-pokemon

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the test suite
pytest
```

## Running the server

Start the MCP server which exposes the Pokémon data resource and battle
simulation tool:

```bash
python server.py
```

List available tools and resources using the MCP client of your choice. This server exposes:

- Resource `pokemon`
- Tool `simulate_battle`

## Pokémon Data Resource

The `pokemon` resource follows the MCP resource pattern. It lists available
Pokémon and returns full details for each entry. All information is fetched live
from the public [PokeAPI](https://pokeapi.co/), including base stats, types,
abilities, move details (type, power, accuracy, category and effect) and
evolution data. No local dataset is bundled with the server.

## Examples

Fetch a Pokémon:

```python
from pokemon_mcp.resources import PokemonResource
from pokemon_mcp.schemas import PokemonDetail
from core.repository import get_pokemon

res = PokemonResource()
print(res.get("Pikachu"))
```

Querying any Pokémon fetches data from PokeAPI:

```python
res.get("Lucario")
```

Simulate a battle:

```python
from pokemon_mcp.tools import simulate_battle_tool
from pokemon_mcp.schemas import SimulateRequest

req = SimulateRequest(pokemonA="Pikachu", pokemonB="Squirtle", seed=42)
res = simulate_battle_tool(req)
print(res.winner)
print(res.log[:3])
```

Determinism is guaranteed through a seed parameter (default 42). Reusing the
same seed yields identical battle logs.

## Command-line Battle Simulation

The repository includes a standalone script for simulating battles without
running the MCP server:

```bash
# simulate Pikachu vs. Squirtle at level 50
python simulate_battle.py Pikachu Squirtle --level 50 --seed 123 --max-turns 200
```

The script prints the winner, a turn-by-turn log and the final state. Omit
optional flags to accept default values.

Example `pokemon` resource call:

```json
{
  "id": 25,
  "name": "Pikachu",
  "types": ["Electric"],
  "base_stats": {"hp": 35, "atk": 55, "def": 40, "sp_atk": 50, "sp_def": 50, "speed": 90},
  "abilities": ["Static", "Lightning Rod"],
  "moves": [{"name": "Thunderbolt", "type": "electric", "power": 90, "category": "special", "accuracy": 100, "effect": "may_paralyze"}, ...],
  "evolution": {"pre": "Pichu", "next": "Raichu"}
}
```

## License

Data is for demonstration only.
