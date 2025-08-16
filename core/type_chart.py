from __future__ import annotations

from functools import lru_cache
from typing import Dict, List

import requests


@lru_cache()
def _load_chart() -> Dict[str, Dict[str, float]]:
    chart: Dict[str, Dict[str, float]] = {}
    try:
        resp = requests.get("https://pokeapi.co/api/v2/type?limit=100", timeout=10)
        if resp.status_code != 200:
            return chart
        for entry in resp.json()["results"]:
            tdata = requests.get(entry["url"], timeout=10).json()
            rel = tdata["damage_relations"]
            mapping: Dict[str, float] = {}
            for t in rel["double_damage_to"]:
                mapping[t["name"]] = 2.0
            for t in rel["half_damage_to"]:
                mapping[t["name"]] = 0.5
            for t in rel["no_damage_to"]:
                mapping[t["name"]] = 0.0
            chart[entry["name"]] = mapping
    except Exception:
        return chart
    return chart


def effectiveness(attack_type: str, defender_types: List[str]) -> float:
    """Return multiplier for attack_type against defender_types using PokeAPI data."""
    chart = _load_chart().get(attack_type.lower(), {})
    mult = 1.0
    for d in defender_types:
        mult *= chart.get(d.lower(), 1.0)
    return mult
