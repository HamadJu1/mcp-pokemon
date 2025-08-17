from mcp.server.fastmcp import FastMCP
try:  # Prefer new MCP types if available
    from mcp.types import Message, TextContent
except ImportError:  # Backward compatibility for older MCP versions
    from mcp.server.fastmcp.prompts.base import Message, TextContent

# Existing domain functions and models
from core.repository import get_evolution, get_move, get_pokemon, list_pokemon

try:
    # Pydantic v2 models preferred
    from pokemon_mcp.schemas import PokemonDetail, PokemonSummary
    V2 = hasattr(PokemonDetail, "model_dump")
except Exception:
    raise


server = FastMCP()

def _to_dict(model: object) -> dict:
    """Return JSON-serializable dict regardless of Pydantic v2/v1."""
    if hasattr(model, "model_dump"):
        return model.model_dump()
    if hasattr(model, "dict"):
        return model.dict()
    return dict(model)


@server.resource("pokemon://list")
async def list_pokemon_resource() -> dict:
    """Return a list of Pokemon summaries."""
    items: list[dict] = [
        _to_dict(PokemonSummary(id=p["id"], name=p["name"], types=p["types"]))
        for p in list_pokemon()
    ]
    return {"items": items}


@server.resource("pokemon://detail/{id}")
async def get_pokemon_resource(id: str) -> dict:
    """Return a Pokemon detail by numeric ID or name."""
    key = int(id) if id.isdigit() else id
    p = get_pokemon(key)
    if not p:
        raise ValueError(f"Pokemon '{id}' not found")

    moves = [m for m in (get_move(mk) for mk in p["moves"]) if m]
    types = [t.capitalize() for t in p["types"]]
    evo = get_evolution(p["name"])

    detail = PokemonDetail(
        id=p["id"],
        name=p["name"],
        types=types,
        base_stats=p["base_stats"],
        abilities=p["abilities"],
        moves=moves,
        evolution=evo,
    )
    return _to_dict(detail)


@server.tool()
async def simulate_battle(
    pokemonA: str,
    pokemonB: str,
    level: int = 50,
    seed: int = 42,
    maxTurns: int = 200,
) -> dict:
    """
    Run a full battle simulation and return a structured result:
    {"winner": str, "turns": int, "log": List[...]}
    """
    from pokemon_mcp.tools import simulate_battle_tool
    from pokemon_mcp.schemas import SimulateRequest

    req = SimulateRequest(
        pokemonA=pokemonA,
        pokemonB=pokemonB,
        level=level,
        seed=seed,
        maxTurns=maxTurns,
    )
    res = simulate_battle_tool(req)

    return {
        "winner": getattr(res, "winner", None),
        "turns": getattr(res, "turns", None),
        "log": getattr(res, "log", []),
    }


@server.prompt("battle-strategy")
def battle_strategy(pokemonA: str, pokemonB: str) -> list[Message]:
    system_msg = Message(
        role="system",
        content=[
            TextContent(
                type="text",
                text=(
                    "You are a concise, tactical Pokémon battle analyst. "
                    "Favor accurate type matchups, realistic movesets, and step-by-step reasoning."
                ),
            )
        ],
    )
    user_msg = Message(
        role="user",
        content=[
            TextContent(
                type="text",
                text=(
                    f"""
Analyze {pokemonA} vs {pokemonB}.
1) Types, key resistances/immunities, and expected effectiveness.
2) 3–4 optimal moves each (move name + why).
3) Viable status plays (burn/poison/paralysis): when and why.
4) Speed/turn-order considerations and pivotal damage thresholds.
5) Likely win path for each side and one high-risk tech option.
Return a compact plan with bullet points and a final one-paragraph verdict.
"""
                ),
            )
        ],
    )
    return [system_msg, user_msg]


@server.prompt("move-explainer")
def move_explainer(moveName: str) -> list[Message]:
    system_msg = Message(
        role="system",
        content=[TextContent(type="text", text="You are a Pokémon move encyclopedia, explaining mechanics clearly.")],
    )
    user_msg = Message(
        role="user",
        content=[
            TextContent(
                type="text",
                text=(
                    f"""
Explain the move: {moveName}.
Include:
- Type and category (physical/special/status)
- Base power and accuracy
- PP
- Key competitive uses
- Notable Pokémon that learn it
Return a structured explanation in bullet points.
"""
                ),
            )
        ],
    )
    return [system_msg, user_msg]


@server.prompt("evolution-guide")
def evolution_guide(pokemonName: str) -> list[Message]:
    system_msg = Message(
        role="system",
        content=[TextContent(type="text", text="You are a knowledgeable Pokémon professor explaining evolutions.")],
    )
    user_msg = Message(
        role="user",
        content=[
            TextContent(
                type="text",
                text=(
                    f"""
Explain how {pokemonName} evolves.
Include:
- Evolution chain with names
- Methods (level, items, friendship, trade, etc.)
- Competitive implications of each stage
- One interesting trivia fact
"""
                ),
            )
        ],
    )
    return [system_msg, user_msg]


@server.prompt("type-matchup")
def type_matchup(typeA: str, typeB: str) -> list[Message]:
    system_msg = Message(
        role="system",
        content=[TextContent(type="text", text="You are a Pokémon type chart analyst.")],
    )
    user_msg = Message(
        role="user",
        content=[
            TextContent(
                type="text",
                text=(
                    f"""
Analyze type matchup: {typeA} vs {typeB}.
Include:
- Effectiveness multipliers (super-effective, not very effective, immune)
- Example Pokémon that embody each type
- Typical strategies when these types face each other
- Competitive history or common meta insights
"""
                ),
            )
        ],
    )
    return [system_msg, user_msg]


@server.prompt("quick-trivia")
def quick_trivia(topic: str) -> list[Message]:
    system_msg = Message(
        role="system",
        content=[TextContent(type="text", text="You are a fun Pokémon trivia master.")],
    )
    user_msg = Message(
        role="user",
        content=[
            TextContent(
                type="text",
                text=(
                    f"""
Give me 3–4 short trivia facts about {topic}.
Each fact should be surprising, concise, and accurate.
End with one one-sentence fun fact.
"""
                ),
            )
        ],
    )
    return [system_msg, user_msg]


if __name__ == "__main__":
    server.run()
