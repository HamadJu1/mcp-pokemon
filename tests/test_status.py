from random import Random

from core.damage import calc_damage
from core.repository import get_move, get_pokemon
from core.status import end_of_turn
from core.turn_engine import simulate_battle


def test_dot_application():
    assert end_of_turn("burn", 160, 160) == 150
    assert end_of_turn("poison", 160, 160) == 140


def test_burn_attack_penalty():
    charizard = get_pokemon("Charizard")
    venusaur = get_pokemon("Venusaur")
    move = get_move("Dragon Claw")
    normal = calc_damage(charizard, venusaur, move, 50, Random(42))
    burned = calc_damage(charizard, venusaur, move, 50, Random(42), attacker_status="burn")
    assert burned < normal


def test_paralysis_skip_deterministic():
    pikachu = get_pokemon("Pikachu")
    squirtle = get_pokemon("Squirtle")
    result = simulate_battle(pikachu, squirtle, seed=1, status_a="paralyze", max_turns=1)
    assert result["log"][0]["skip"] is True
