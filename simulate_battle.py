import argparse

from mcp.tools import simulate_battle_tool
from mcp.schemas import SimulateRequest


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate a Pokémon battle")
    parser.add_argument("pokemonA", help="Name of the first Pokémon")
    parser.add_argument("pokemonB", help="Name of the second Pokémon")
    parser.add_argument("--level", type=int, default=50, help="Battle level (1-100)")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for determinism")
    parser.add_argument(
        "--max-turns",
        type=int,
        default=200,
        dest="max_turns",
        help="Maximum number of turns to simulate",
    )
    args = parser.parse_args()

    req = SimulateRequest(
        pokemonA=args.pokemonA,
        pokemonB=args.pokemonB,
        level=args.level,
        seed=args.seed,
        maxTurns=args.max_turns,
    )
    res = simulate_battle_tool(req)

    print(f"Winner: {res.winner} after {res.turns} turns")
    for entry in res.log:
        move = entry.move or "skip"
        print(
            f"Turn {entry.turn}: {entry.actor} used {move} on {entry.target} "
            f"for {entry.damage} damage (effectiveness {entry.effectiveness})"
        )
        if entry.statusApplied:
            print(f"  Status applied: {entry.statusApplied}")
        print(f"  HP after: {entry.hpAfter}")

    print("Final state:", res.finalState)


if __name__ == "__main__":
    main()
