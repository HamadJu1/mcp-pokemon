from core.type_chart import effectiveness


def test_fire_vs_grass():
    assert effectiveness("fire", ["grass"]) == 2.0


def test_electric_vs_ground():
    assert effectiveness("electric", ["ground"]) == 0.0


def test_water_vs_rock_ground():
    assert effectiveness("water", ["rock", "ground"]) == 4.0


def test_ghost_vs_normal():
    assert effectiveness("ghost", ["normal"]) == 0.0


def test_grass_vs_fire():
    assert effectiveness("grass", ["fire"]) == 0.5
