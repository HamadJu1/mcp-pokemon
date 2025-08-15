from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Dict, List, Optional

from .damage import calc_damage
from .repository import get_move
from .status import apply_status, end_of_turn
from .type_chart import effectiveness


@dataclass
class BattleState:
    pokemon: Dict
    hp: int
    status: Optional[str] = None

    @property
    def max_hp(self) -> int:
        return self.pokemon["base_stats"]["hp"]


def _score_move(attacker: Dict, defender: Dict, move: Dict) -> float:
    power = move.get("power", 0)
    if power == 0:
        return 0.0
    stab = 1.5 if move["type"] in [t.lower() for t in attacker["types"]] else 1.0
    eff = effectiveness(move["type"], defender["types"])
    acc = move.get("accuracy", 100) / 100
    return power * eff * stab * acc


def _choose_move(attacker: Dict, defender: Dict) -> Dict:
    best = None
    best_score = -1.0
    for name in attacker["moves"]:
        move = get_move(name)
        score = _score_move(attacker, defender, move)
        if score > best_score:
            best = move
            best_score = score
    return best


def simulate_battle(pokemon_a: Dict, pokemon_b: Dict, level: int = 50, seed: int = 42, max_turns: int = 200, status_a: Optional[str] = None, status_b: Optional[str] = None) -> Dict:
    rng = Random(seed)
    a_state = BattleState(pokemon_a, pokemon_a["base_stats"]["hp"], status_a)
    b_state = BattleState(pokemon_b, pokemon_b["base_stats"]["hp"], status_b)
    log: List[Dict] = []

    for turn in range(1, max_turns + 1):
        order = [(a_state, b_state), (b_state, a_state)]
        speed_a = a_state.pokemon["base_stats"]["speed"]
        if a_state.status == "paralyze":
            speed_a /= 2
        speed_b = b_state.pokemon["base_stats"]["speed"]
        if b_state.status == "paralyze":
            speed_b /= 2
        if speed_b > speed_a:
            order = order[::-1]
        elif speed_a == speed_b and rng.random() >= 0.5:
            order = order[::-1]

        for actor, target in order:
            if actor.hp <= 0 or target.hp <= 0:
                continue
            if actor.status == "paralyze" and rng.random() < 0.25:
                log.append(
                    {
                        "turn": turn,
                        "actor": actor.pokemon["name"],
                        "target": target.pokemon["name"],
                        "move": None,
                        "effectiveness": 0.0,
                        "damage": 0,
                        "skip": True,
                        "statusApplied": None,
                        "hpAfter": {
                            a_state.pokemon["name"]: a_state.hp,
                            b_state.pokemon["name"]: b_state.hp,
                        },
                    }
                )
                continue
            move = _choose_move(actor.pokemon, target.pokemon)
            hit = rng.uniform(0, 100) <= move.get("accuracy", 100)
            status_applied = None
            if hit:
                damage = calc_damage(actor.pokemon, target.pokemon, move, level, rng, actor.status)
                target.hp = max(target.hp - damage, 0)
                effect = move.get("effect")
                if effect in {"burn", "poison", "paralyze"}:
                    new_status = apply_status(target.status, effect)
                    if new_status != target.status:
                        target.status = new_status
                        status_applied = new_status
            else:
                damage = 0
            log.append(
                {
                    "turn": turn,
                    "actor": actor.pokemon["name"],
                    "target": target.pokemon["name"],
                    "move": move["name"],
                    "effectiveness": effectiveness(move["type"], target.pokemon["types"]),
                    "damage": damage,
                    "skip": False,
                    "statusApplied": status_applied,
                    "hpAfter": {
                        a_state.pokemon["name"]: a_state.hp,
                        b_state.pokemon["name"]: b_state.hp,
                    },
                }
            )
            if target.hp <= 0:
                winner = actor.pokemon["name"]
                return {
                    "winner": winner,
                    "turns": turn,
                    "log": log,
                    "finalState": {
                        a_state.pokemon["name"]: a_state.hp,
                        b_state.pokemon["name"]: b_state.hp,
                    },
                }
        # end-of-turn statuses
        a_state.hp = end_of_turn(a_state.status, a_state.max_hp, a_state.hp)
        b_state.hp = end_of_turn(b_state.status, b_state.max_hp, b_state.hp)
        if a_state.hp <= 0 or b_state.hp <= 0:
            winner = a_state.pokemon["name"] if a_state.hp > b_state.hp else b_state.pokemon["name"]
            return {
                "winner": winner,
                "turns": turn,
                "log": log,
                "finalState": {
                    a_state.pokemon["name"]: a_state.hp,
                    b_state.pokemon["name"]: b_state.hp,
                },
            }
    return {
        "winner": a_state.pokemon["name"] if a_state.hp > b_state.hp else b_state.pokemon["name"],
        "turns": max_turns,
        "log": log,
        "finalState": {
            a_state.pokemon["name"]: a_state.hp,
            b_state.pokemon["name"]: b_state.hp,
        },
    }
