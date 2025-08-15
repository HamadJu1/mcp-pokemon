import asyncio

from pokemon_mcp.resources import PokemonResource


async def _fetch(name: str):
    res = PokemonResource()
    return await res.get(name)


def test_pokemon_resource_shape():
    data = asyncio.get_event_loop().run_until_complete(_fetch("Pikachu"))
    assert data["id"] == 25
    assert data["name"] == "Pikachu"
    assert data["types"] == ["Electric"]
    stats = data["base_stats"]
    assert set(stats.keys()) == {"hp", "atk", "def", "sp_atk", "sp_def", "speed"}
    assert all(isinstance(v, int) for v in stats.values())
    assert "Static" in data["abilities"]
    move = next(m for m in data["moves"] if m["name"] == "Thunderbolt")
    assert move["effect"] == "may_paralyze"
    assert move["type"] == "electric"
    evo = data["evolution"]
    assert evo == {"pre": "Pichu", "next": "Raichu"}
