import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

pokemon = json.load(open(DATA / "pokemon_index.json"))
moves = {m["name"]: m for m in json.load(open(DATA / "moves.json"))}

def test_moves_cross_reference():
    for p in pokemon:
        for name in p["moves"]:
            assert name in moves, f"{p['name']} references unknown move {name}"
            mv = moves[name]
            for field in ["type", "power", "category", "accuracy"]:
                assert field in mv, f"move {name} missing {field}"
            if mv["category"] == "status" or mv["power"] == 0:
                assert "effect" in mv, f"status move {name} missing effect"
