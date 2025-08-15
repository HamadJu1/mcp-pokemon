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

## Examples

Fetch a Pokémon:

```python
from mcp.resources import PokemonResource
from mcp.schemas import PokemonDetail
from core.repository import get_pokemon

res = PokemonResource()
print(res.get("Pikachu"))
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

## License

Data is for demonstration only. Pokémon and names are trademarks of Nintendo and Game Freak.
