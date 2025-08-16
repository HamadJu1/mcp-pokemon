# Pokémon Resource

This repository exposes a single MCP resource named `pokemon`. All data is
retrieved on demand from the public [PokeAPI](https://pokeapi.co/) with no local
copies.

## Listing Pokémon

An LLM can request a list of available Pokémon:

```xml
<assistant to="pokemon:list">
{}
</assistant>
```

The server responds with summaries including id, name and types.

## Fetching Details

Request full information about a specific Pokémon by id or name:

```xml
<assistant to="pokemon:get">
{"id": "Pikachu"}
</assistant>
```

The response includes base stats, abilities, **all available moves with their
type, power, accuracy, category and effect**, plus evolution information as
provided by PokeAPI.

### Example Conversation

```xml
<user>Tell me about Pikachu</user>
<assistant to="pokemon:get">{"id": "Pikachu"}</assistant>
<tool name="pokemon:get">
  {"id":25,"name":"Pikachu","types":["Electric"],"base_stats":{"hp":35,"atk":55,"def":40,"sp_atk":50,"sp_def":50,"speed":90},"abilities":["Static","Lightning Rod"],"moves":[{"name":"Quick Attack","type":"normal","power":40,"category":"physical","accuracy":100,"effect":"no additional effect"}, ...],"evolution":{"pre":"Pichu","next":"Raichu"}}
</tool>
<assistant>Pikachu is an Electric-type Pokémon. One of its moves, Quick Attack, is a normal move with 40 power that always strikes first.</assistant>
```

## Usage Notes

- Names are case-insensitive; both `"25"` and `"Pikachu"` work.
- The list endpoint returns the first 151 Pokémon for quick exploration.
- Since data is fetched live from PokeAPI, clients may cache results to avoid
  repeated network calls.
