# MCP Pokémon

A minimal deterministic Pokémon battle simulator wrapped in an MCP server.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the server

```bash
python server.py
```

List available tools and resources using the MCP client of your choice. This server exposes:

- Resource `pokemon`
- Tool `simulate_battle`

## Pokémon Data Resource

The `pokemon` resource follows the MCP resource pattern. It lists available
Pokémon and returns full details for each entry. When a Pokémon is not present
in the bundled dataset, the resource connects to the public [PokeAPI](https://pokeapi.co/)
to retrieve up-to-date information including base stats, types, abilities, moves
and evolution data.

## Examples

Fetch a Pokémon:

```python
from mcp.resources import PokemonResource
from mcp.schemas import PokemonDetail
from core.repository import get_pokemon

res = PokemonResource()
print(res.get("Pikachu"))
```

Querying a Pokémon not in the local dataset triggers a fetch from PokeAPI:

```python
res.get("Lucario")
```

Simulate a battle:

```python
from mcp.tools import simulate_battle_tool
from mcp.schemas import SimulateRequest

req = SimulateRequest(pokemonA="Pikachu", pokemonB="Squirtle", seed=42)
res = simulate_battle_tool(req)
print(res.winner)
print(res.log[:3])
```

Determinism is guaranteed through a seed parameter (default 42). Reusing the same seed yields identical battle logs.

## Data

Core datasets are stored locally under `data/` and compiled from public information.
When a requested Pokémon or move is missing, data is fetched live from PokeAPI.
Pokémon and names are trademarks of Nintendo and Game Freak.

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
