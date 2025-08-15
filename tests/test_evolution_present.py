import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

pokemon = json.load(open(DATA / "pokemon_index.json"))
evos = json.load(open(DATA / "evolutions.json"))

NO_EVOLUTION = {"Mewtwo"}

def test_evolution_entries():
    for p in pokemon:
        ev = evos.get(p["name"])
        assert ev is not None, f"missing evolution for {p['name']}"
        if p["name"] not in NO_EVOLUTION:
            assert ev.get("pre") or ev.get("next"), f"{p['name']} missing pre/next"
