from pokemon_mcp.tools import simulate_battle_tool


def test_simulate_battle_api():
    res = simulate_battle_tool(pokemonA="Pikachu", pokemonB="Squirtle", seed=42)
    assert res.winner == "Pikachu"
    assert res.turns == 1
    assert len(res.log) == 1
    first = res.log[0]
    assert first.actor == "Pikachu"
    assert first.move == "Thunderbolt"
    assert first.effectiveness == 2.0
