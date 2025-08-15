import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"

pokemon = json.load(open(BASE / "pokemon_index.json"))
moves = {m["name"]: m for m in json.load(open(BASE / "moves.json"))}
types = set(json.load(open(BASE / "types.json")).keys())
evos = json.load(open(BASE / "evolutions.json"))

errors = []

for p in pokemon:
    name = p["name"]
    stats = p.get("base_stats", {})
    required_stats = {"hp", "atk", "def", "sp_atk", "sp_def", "speed"}
    if set(stats.keys()) != required_stats:
        errors.append(f"{name} base_stats incomplete")
    for t in p.get("types", []):
        if t.lower() not in types:
            errors.append(f"{name} unknown type {t}")
    if not p.get("abilities"):
        errors.append(f"{name} missing abilities")
    for mv_name in p.get("moves", []):
        mv = moves.get(mv_name)
        if not mv:
            errors.append(f"{name} unknown move {mv_name}")
            continue
        for field in ["type", "power", "category", "accuracy"]:
            if field not in mv:
                errors.append(f"move {mv_name} missing {field}")
        if mv["type"].lower() not in types:
            errors.append(f"move {mv_name} has unknown type {mv['type']}")
        if mv["category"] == "status" or mv["power"] == 0:
            if "effect" not in mv:
                errors.append(f"status move {mv_name} missing effect")
    evo = evos.get(name)
    if evo is None:
        errors.append(f"{name} missing evolution entry")
    else:
        if evo and not (evo.get("pre") or evo.get("next")):
            errors.append(f"{name} evolution missing pre/next")

if errors:
    for e in errors:
        print("ERROR:", e)
    sys.exit(1)

print("Data OK")
