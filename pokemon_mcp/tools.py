from __future__ import annotations

from pokemon_mcp.server import Tool

from core.repository import get_pokemon
from core.turn_engine import simulate_battle
from legacy_server import server
from .schemas import SimulateRequest, SimulateResponse


@server.tool("simulate_battle")
def simulate_battle_tool(params: SimulateRequest) -> SimulateResponse:
    a = get_pokemon(params.pokemonA)
    b = get_pokemon(params.pokemonB)
    result = simulate_battle(a, b, level=params.level, seed=params.seed, max_turns=params.maxTurns)
    return SimulateResponse(**result)
