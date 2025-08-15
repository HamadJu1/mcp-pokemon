from random import Random

from core.damage import calc_damage
from core.repository import get_move, get_pokemon


def test_pikachu_thunderbolt_squirtle():
    rng = Random(42)
    pikachu = get_pokemon("Pikachu")
    squirtle = get_pokemon("Squirtle")
    move = get_move("Thunderbolt")
    assert calc_damage(pikachu, squirtle, move, 50, rng) == 93


def test_charizard_flamethrower_venusaur():
    rng = Random(42)
    charizard = get_pokemon("Charizard")
    venusaur = get_pokemon("Venusaur")
    move = get_move("Flamethrower")
    assert calc_damage(charizard, venusaur, move, 50, rng) == 128


def test_onix_rockslide_charizard():
    rng = Random(42)
    onix = get_pokemon("Onix")
    charizard = get_pokemon("Charizard")
    move = get_move("Rock Slide")
    assert calc_damage(onix, charizard, move, 50, rng) == 119


def test_machamp_closecombat_gengar_immunity():
    rng = Random(42)
    machamp = get_pokemon("Machamp")
    gengar = get_pokemon("Gengar")
    move = get_move("Close Combat")
    assert calc_damage(machamp, gengar, move, 50, rng) == 0
