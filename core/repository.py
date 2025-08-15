from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_json(name: str) -> Any:
    with (DATA_DIR / name).open() as f:
        return json.load(f)


_POKEMON_INDEX: List[Dict[str, Any]] = _load_json("pokemon_index.json")
_MOVES: Dict[str, Dict[str, Any]] = {m["name"]: m for m in _load_json("moves.json")}
_TYPES: Dict[str, Dict[str, float]] = _load_json("types.json")
_EVOS: Dict[str, Dict[str, Any]] = _load_json("evolutions.json")


def get_pokemon(identifier: str | int) -> Optional[Dict[str, Any]]:
    for p in _POKEMON_INDEX:
        if isinstance(identifier, int) and p["id"] == identifier:
            return dict(p)
        if isinstance(identifier, str) and p["name"].lower() == identifier.lower():
            return dict(p)

    # Fallback to the public PokeAPI if the Pokémon is not in the local index
    name = str(identifier).lower()
    try:
        resp = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}", timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        stats = {
            s["stat"]["name"].replace("-", "_"): s["base_stat"] for s in data["stats"]
        }
        abilities = [
            a["ability"]["name"].replace("-", " ").title() for a in data["abilities"]
        ]
        types = [t["type"]["name"] for t in data["types"]]
        move_names = [m["move"]["name"].replace("-", " ").title() for m in data["moves"][:4]]
        evo = get_evolution(data["name"])
        return {
            "id": data["id"],
            "name": data["name"].title(),
            "types": types,
            "base_stats": {
                "hp": stats.get("hp"),
                "atk": stats.get("attack"),
                "def": stats.get("defense"),
                "sp_atk": stats.get("special_attack"),
                "sp_def": stats.get("special_defense"),
                "speed": stats.get("speed"),
            },
            "abilities": abilities,
            "moves": move_names,
            "evolution": evo,
        }
    except Exception:
        return None


def get_move(name: str) -> Optional[Dict[str, Any]]:
    move = _MOVES.get(name)
    if move:
        return move

    api_name = name.lower().replace(" ", "-")
    try:
        resp = requests.get(f"https://pokeapi.co/api/v2/move/{api_name}", timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        effect = None
        for entry in data.get("effect_entries", []):
            if entry["language"]["name"] == "en":
                effect = entry.get("short_effect")
                break
        move = {
            "name": data["name"].replace("-", " ").title(),
            "type": data["type"]["name"],
            "power": data["power"],
            "category": data["damage_class"]["name"],
            "accuracy": data["accuracy"],
            "effect": effect,
        }
        _MOVES[move["name"]] = move
        return move
    except Exception:
        return None


def list_pokemon() -> List[Dict[str, Any]]:
    return _POKEMON_INDEX


def get_evolution(name: str) -> Dict[str, Any]:
    evo = _EVOS.get(name)
    if evo:
        return evo

    # Query PokeAPI for evolution data
    try:
        resp = requests.get(
            f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}", timeout=10
        )
        if resp.status_code != 200:
            return {}
        species = resp.json()
        result: Dict[str, Any] = {}
        if species.get("evolves_from_species"):
            result["pre"] = species["evolves_from_species"]["name"].title()

        chain_resp = requests.get(species["evolution_chain"]["url"], timeout=10)
        chain = chain_resp.json()["chain"]

        def _find(chain: Dict[str, Any]) -> List[str]:
            if chain["species"]["name"] == name.lower():
                return [e["species"]["name"] for e in chain["evolves_to"]]
            for e in chain["evolves_to"]:
                res = _find(e)
                if res:
                    return res
            return []

        next_evos = _find(chain)
        if next_evos:
            formatted = [n.title() for n in next_evos]
            result["next"] = formatted[0] if len(formatted) == 1 else formatted

        _EVOS[name] = result
        return result
    except Exception:
        return {}
