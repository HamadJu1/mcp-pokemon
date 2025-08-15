from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TYPE_CHART_PATH = DATA_DIR / "types.json"

with TYPE_CHART_PATH.open() as f:
    _TYPE_CHART: Dict[str, Dict[str, float]] = json.load(f)


def effectiveness(attack_type: str, defender_types: List[str]) -> float:
    """Return multiplier for attack_type against defender_types."""
    atk = attack_type.lower()
    mult = 1.0
    chart = _TYPE_CHART.get(atk, {})
    for d in defender_types:
        mult *= chart.get(d.lower(), 1.0)
    return mult
