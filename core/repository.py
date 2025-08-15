from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_json(name: str) -> Any:
    with (DATA_DIR / name).open() as f:
        return json.load(f)


_POKEMON_INDEX: List[Dict[str, Any]] = _load_json("pokemon_index.json")
_MOVES: Dict[str, Dict[str, Any]] = {m["name"]: m for m in _load_json("moves.json")}
_TYPES: Dict[str, Dict[str, float]] = _load_json("types.json")
_EVOS: Dict[str, str] = _load_json("evolutions.json")


def get_pokemon(identifier: str | int) -> Optional[Dict[str, Any]]:
    for p in _POKEMON_INDEX:
        if isinstance(identifier, int) and p["id"] == identifier:
            return p
        if isinstance(identifier, str) and p["name"].lower() == identifier.lower():
            return p
    return None


def get_move(name: str) -> Optional[Dict[str, Any]]:
    return _MOVES.get(name)


def list_pokemon() -> List[Dict[str, Any]]:
    return _POKEMON_INDEX


def get_evolution(name: str) -> Optional[str]:
    return _EVOS.get(name)
