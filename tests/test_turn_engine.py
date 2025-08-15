from core.repository import get_pokemon
from core.turn_engine import simulate_battle


def test_winner_for_type_advantage():
    charizard = get_pokemon("Charizard")
    venusaur = get_pokemon("Venusaur")
    result = simulate_battle(charizard, venusaur, seed=42)
    assert result["winner"] == "Charizard"


def test_speed_tie_breaker():
    dragonite = get_pokemon("Dragonite")
    venusaur = get_pokemon("Venusaur")
    result = simulate_battle(dragonite, venusaur, seed=42)
    assert result["log"][0]["actor"] == "Venusaur"
    assert result["winner"] == "Dragonite"


def test_paralysis_speed_penalty():
    pikachu = get_pokemon("Pikachu")
    wartortle = get_pokemon("Wartortle")
    result = simulate_battle(pikachu, wartortle, seed=42, status_a="paralyze")
    assert result["log"][0]["actor"] == "Wartortle"
