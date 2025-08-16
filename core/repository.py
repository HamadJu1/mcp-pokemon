from __future__ import annotations

from typing import Any, Dict, List, Optional

import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# In-memory caches to avoid repeated network calls
_POKEMON_CACHE: Dict[str, Dict[str, Any]] = {}
_MOVE_CACHE: Dict[str, Dict[str, Any]] = {}
_POKEMON_INDEX: List[Dict[str, Any]] | None = None
_EVOLUTION_CACHE: Dict[str, Dict[str, Any]] = {}

# Shared HTTP session for PokeAPI calls
POKEAPI_TIMEOUT = float(os.getenv("POKEAPI_TIMEOUT", "10"))
SESSION = requests.Session()
_retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
_adapter = HTTPAdapter(max_retries=_retries)
SESSION.mount("http://", _adapter)
SESSION.mount("https://", _adapter)



def get_pokemon(identifier: str | int) -> Optional[Dict[str, Any]]:
    """Fetch a Pokémon by name or id from PokeAPI."""
    key = str(identifier).lower()
    cached = _POKEMON_CACHE.get(key)
    if cached:
        return cached

    try:
        resp = SESSION.get(
            f"https://pokeapi.co/api/v2/pokemon/{key}", timeout=POKEAPI_TIMEOUT
        )
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
        move_names = [
            m["move"]["name"].replace("-", " ").title() for m in data["moves"]
        ]
        evo = get_evolution(data["name"])
        result = {
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
        _POKEMON_CACHE[key] = result
        _POKEMON_CACHE[str(result["id"])] = result
        return result
    except Exception:
        return None


def get_move(name: str) -> Optional[Dict[str, Any]]:
    """Fetch move data from PokeAPI."""
    move = _MOVE_CACHE.get(name)
    if move:
        return move

    api_name = name.lower().replace(" ", "-")
    try:
        resp = SESSION.get(
            f"https://pokeapi.co/api/v2/move/{api_name}", timeout=POKEAPI_TIMEOUT
        )
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
        _MOVE_CACHE[move["name"]] = move
        return move
    except Exception:
        return None


def list_pokemon() -> List[Dict[str, Any]]:
    """Return a list of Pokémon summaries from PokeAPI."""
    global _POKEMON_INDEX
    if _POKEMON_INDEX is not None:
        return _POKEMON_INDEX

    try:
        resp = SESSION.get(
            "https://pokeapi.co/api/v2/pokemon?limit=151", timeout=POKEAPI_TIMEOUT
        )
        if resp.status_code != 200:
            return []
        results = resp.json()["results"]
        index: List[Dict[str, Any]] = []
        for item in results:
            detail = get_pokemon(item["name"])
            if detail:
                index.append(
                    {"id": detail["id"], "name": detail["name"], "types": detail["types"]}
                )
        _POKEMON_INDEX = index
        return index
    except Exception:
        return []


def get_evolution(name: str) -> Dict[str, Any]:
    """Fetch evolution info for a Pokémon from PokeAPI."""
    cached = _EVOLUTION_CACHE.get(name)
    if cached is not None:
        return cached

    try:
        resp = SESSION.get(
            f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}",
            timeout=POKEAPI_TIMEOUT,
        )
        if resp.status_code != 200:
            return {}
        species = resp.json()
        result: Dict[str, Any] = {}
        if species.get("evolves_from_species"):
            result["pre"] = species["evolves_from_species"]["name"].title()

        chain_resp = SESSION.get(
            species["evolution_chain"]["url"], timeout=POKEAPI_TIMEOUT
        )
        chain = chain_resp.json()["chain"]

        def _find(node: Dict[str, Any]) -> List[str]:
            if node["species"]["name"] == name.lower():
                return [e["species"]["name"] for e in node["evolves_to"]]
            for e in node["evolves_to"]:
                res = _find(e)
                if res:
                    return res
            return []

        next_evos = _find(chain)
        if next_evos:
            formatted = [n.title() for n in next_evos]
            result["next"] = formatted[0] if len(formatted) == 1 else formatted

        _EVOLUTION_CACHE[name] = result
        return result
    except Exception:
        return {}
