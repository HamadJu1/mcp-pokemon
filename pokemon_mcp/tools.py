from __future__ import annotations

from pokemon_mcp.server import Tool

from core.repository import get_pokemon
from core.turn_engine import simulate_battle
from legacy_server import server
from .schemas import SimulateRequest, SimulateResponse


@server.tool("simulate_battle")
def simulate_battle_tool(
    pokemonA: str,
    pokemonB: str,
    level: int = 50,
    seed: int = 42,
    maxTurns: int = 200,
) -> SimulateResponse:
    """Simulate a battle between two Pokémon.

    Args:
        pokemonA: Name of the first Pokémon.
        pokemonB: Name of the second Pokémon.
        level: Battle level (1-100).
        seed: RNG seed for determinism.
        maxTurns: Maximum number of turns to simulate.
    """

    req = SimulateRequest(
        pokemonA=pokemonA,
        pokemonB=pokemonB,
        level=level,
        seed=seed,
        maxTurns=maxTurns,
    )

    a = get_pokemon(req.pokemonA)
    b = get_pokemon(req.pokemonB)
    result = simulate_battle(
        a, b, level=req.level, seed=req.seed, max_turns=req.maxTurns
    )
    return SimulateResponse(**result)
