from __future__ import annotations

import math
from random import Random
from typing import Dict, Optional

from .type_chart import effectiveness


def calc_damage(attacker: Dict, defender: Dict, move: Dict, level: int, rng: Random, attacker_status: Optional[str] = None) -> int:
    if move.get("power", 0) == 0:
        return 0
    category = move.get("category", "physical")
    power = move["power"]
    if category == "physical":
        atk = attacker["base_stats"]["atk"]
        if attacker_status == "burn":
            atk *= 0.5
        defense = defender["base_stats"]["def"]
    else:
        atk = attacker["base_stats"]["sp_atk"]
        defense = defender["base_stats"]["sp_def"]
    base = (((2 * level / 5 + 2) * power * (atk / defense)) / 50) + 2
    stab = 1.5 if move["type"] in [t.lower() for t in attacker["types"]] else 1.0
    type_mult = effectiveness(move["type"], defender["types"])
    rand = rng.uniform(0.85, 1.0)
    return math.floor(base * stab * type_mult * rand)
