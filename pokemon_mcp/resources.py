from __future__ import annotations

from typing import Any, Dict, Optional

from pokemon_mcp.server import Resource

from core.repository import get_move, get_pokemon, list_pokemon
from .schemas import PokemonDetail, PokemonSummary
from legacy_server import server


@server.resource("pokemon")
class PokemonResource(Resource):
    async def list(self, cursor: Optional[str] = None) -> Dict[str, Any]:
        items = [
            PokemonSummary(id=p["id"], name=p["name"], types=p["types"]).dict()
            for p in list_pokemon()
        ]
        return {"items": items}

    async def get(self, id: str) -> Dict[str, Any]:
        key: Any = int(id) if id.isdigit() else id
        p = get_pokemon(key)
        if not p:
            raise KeyError("not found")
        moves = []
        for name in p["moves"]:
            mv = get_move(name)
            if mv:
                moves.append(mv)
        types = [t.capitalize() for t in p["types"]]
        detail = PokemonDetail(
            id=p["id"],
            name=p["name"],
            types=types,
            base_stats=p["base_stats"],
            abilities=p["abilities"],
            moves=moves,
            evolution=p["evolution"],
        )
        return detail.dict()
