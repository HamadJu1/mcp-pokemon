from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class StatusState:
    name: str
    turns: int = 0


def apply_status(current: Optional[str], new_status: Optional[str]) -> Optional[str]:
    if current is None:
        return new_status
    return current


def end_of_turn(status: Optional[str], max_hp: int, hp: int) -> int:
    if status == "burn":
        hp -= max(1, max_hp // 16)
    elif status == "poison":
        hp -= max(1, max_hp // 8)
    return max(hp, 0)
