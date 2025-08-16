# Pokémon Resource

This repository exposes Pokémon data to MCP clients through a resource named `pokemon`.
It follows the [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol) resource design, providing deterministic responses that are suitable for LLM consumption.

## Overview

The resource is registered on the server with:

```python
@server.resource("pokemon")
class PokemonResource(Resource):
    ...
```

The resource offers two methods:

- `list(cursor: Optional[str] = None)` – returns a collection of Pokémon summaries.
- `get(id: str)` – returns full details for a specific Pokémon by name or numeric ID.

## Listing Pokémon

`list()` returns an object with an `items` field containing `PokemonSummary` objects:

```json
{
  "items": [
    {"id": 1, "name": "Bulbasaur", "types": ["Grass", "Poison"]},
    {"id": 4, "name": "Charmander", "types": ["Fire"]}
  ]
}
```

This data is generated from the local dataset under `data/`.

## Fetching a Pokémon

`get()` accepts either a name or Pokédex ID. It returns a `PokemonDetail` object with base stats, abilities, moves and evolution data. When a Pokémon is not present in the local dataset, details are fetched from the public [PokeAPI](https://pokeapi.co/).

Example:

```python
from pokemon_mcp.resources import PokemonResource

res = PokemonResource()
info = await res.get("Pikachu")
```

Sample response:

```json
{
  "id": 25,
  "name": "Pikachu",
  "types": ["Electric"],
  "base_stats": {"hp": 35, "atk": 55, "def": 40, "sp_atk": 50, "sp_def": 50, "speed": 90},
  "abilities": ["Static", "Lightning Rod"],
  "moves": [{"name": "Thunderbolt", "type": "electric", "power": 90, "category": "special", "accuracy": 100, "effect": "may_paralyze"}],
  "evolution": {"pre": "Pichu", "next": "Raichu"}
}
```

## Notes

- Moves included in the response are filtered to ones available in the local database.
- Evolution data contains optional `pre` and `next` fields, omitted when unavailable.
- Results are deterministic; repeated calls with the same name or ID return the same data.

