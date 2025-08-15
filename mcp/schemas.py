from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SimulateRequest(BaseModel):
    pokemonA: str
    pokemonB: str
    level: int = Field(50, ge=1, le=100)
    seed: int = 42
    maxTurns: int = 200


class LogEntry(BaseModel):
    turn: int
    actor: str
    target: str
    move: Optional[str]
    effectiveness: float
    damage: int
    skip: bool
    statusApplied: Optional[str]
    hpAfter: Dict[str, int]


class SimulateResponse(BaseModel):
    winner: str
    turns: int
    log: List[LogEntry]
    finalState: Dict[str, int]


class PokemonSummary(BaseModel):
    id: int
    name: str
    types: List[str]


class MoveDetail(BaseModel):
    name: str
    type: str
    power: int
    category: str
    accuracy: int
    effect: Optional[str] = None


class EvolutionDetail(BaseModel):
    pre: Optional[str] = None
    next: Optional[str] = None


class PokemonDetail(PokemonSummary):
    base_stats: Dict[str, int]
    abilities: List[str]
    moves: List[MoveDetail]
    evolution: EvolutionDetail
