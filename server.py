from mcp.server.fastmcp import FastMCP
import openai
from mcp.server.fastmcp.prompts.base import AssistantMessage

# Existing domain functions and models
from core.repository import get_evolution, get_move, get_pokemon, list_pokemon

try:
    # Pydantic v2 models preferred
    from pokemon_mcp.schemas import PokemonDetail, PokemonSummary, SimulateRequest
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


@server.tool(name="simulate_battle")
async def simulate_battle(params: SimulateRequest) -> dict:
    """Run a battle simulation and return structured JSON."""
    from pokemon_mcp.tools import simulate_battle_tool

    # Apply defaults via the Pydantic model
    req = SimulateRequest(**params.model_dump())  # ensures defaults for missing fields

    try:
        res = simulate_battle_tool(req)
    except Exception as e:  # pragma: no cover - surface as ValueError
        suggestions = [p["name"] for p in list_pokemon()[:2]]
        raise ValueError(
            f"{e}. Try names like {suggestions[0]} or {suggestions[1]}"
        ) from e

    return {
        "winner": res.winner,
        "turns": res.turns,
        "log": [_to_dict(entry) for entry in res.log],
    }


@server.prompt("battle-strategy")
def battle_strategy(pokemonA: str, pokemonB: str) -> list[AssistantMessage]:
    """Generate battle strategies for two Pokémon via OpenAI."""
    response = openai.chat.completions.create(
        model="gpt-5-mini",
        messages=[
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
    )
    content = response.choices[0].message.content
    return [AssistantMessage(content=content)]
