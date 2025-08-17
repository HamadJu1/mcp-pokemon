from mcp.server.fastmcp import FastMCP
import openai
from mcp.server.fastmcp.prompts.base import AssistantMessage

# Existing domain functions and models
from core.repository import get_evolution, get_move, get_pokemon, list_pokemon

try:
    # Pydantic v2 models preferred
    from pokemon_mcp.schemas import PokemonDetail, PokemonSummary
    V2 = hasattr(PokemonDetail, "model_dump")
except Exception:
    raise

openai.api_key = ""

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
def battle_strategy(pokemonA: str, pokemonB: str) -> list[AssistantMessage]:
    """Generate battle strategies for two Pokémon via OpenAI.

    The call leverages the MCP server so the model can explore resources and
    invoke the ``simulate_battle`` tool when forming its response.
    """
    response = openai.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "You are a Pokémon battle expert. Analyze matchups and suggest strategies.",
            },
            {
                "role": "user",
                "content": (
                    f"Simulate a battle between {pokemonA} and {pokemonB}. "
                    "Provide type effectiveness, possible move choices, status effects, and a likely winner."
                ),
            },
        ],
        tools=[{"type": "mcp", "server": server}],
    )
    content = getattr(response, "output_text", "")
    return [AssistantMessage(content=content)]


@server.prompt("simulate-battle")
def simulate_battle_prompt(
    pokemonA: str,
    pokemonB: str,
    level: int = 50,
    seed: int = 42,
    maxTurns: int = 200,
) -> list[AssistantMessage]:
    """Run a full battle simulation via OpenAI using the ``simulate_battle`` tool."""

    response = openai.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Use the `simulate_battle` tool to run Pokémon battles and report the results.",
            },
            {
                "role": "user",
                "content": (
                    f"Simulate {pokemonA} vs {pokemonB} at level {level} with seed {seed} "
                    f"and a maximum of {maxTurns} turns. Summarize the outcome."
                ),
            },
        ],
        tools=[{"type": "mcp", "server": server}],
    )

    content = getattr(response, "output_text", "")
    return [AssistantMessage(content=content)]
