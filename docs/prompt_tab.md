# Prompt Instructions for Battle Simulation

These instructions are loaded into the MCP client's **Prompt** tab. They ensure
that battle questions always invoke the `simulate_battle` tool and never rely on
LLM reasoning.

## Core Guidance

1. When the user asks to simulate or play out a Pokémon battle, always call the
   `simulate_battle` tool exactly once.
2. Pass the parameters provided by the user. Omit any that are unspecified—the
   server supplies defaults for `level`, `seed`, and `maxTurns`. Do **not** wrap
   arguments inside a `params` object; place them directly within `input`.
3. After the tool responds, summarize its JSON output succinctly:
   - state the `winner` and the number of `turns`;
   - list **3–6** notable highlights extracted from the `log` entries.
4. Never fabricate battle outcomes or bypass the tool.
5. If the tool returns an error (e.g., unknown Pokémon), request corrected names
   and suggest two valid alternatives.

## Few‑shot Examples

### Example 1
**User:** "Simulate Bulbasaur vs. Squirtle."

**Assistant (tool call):**
```json
{
  "tool": "simulate_battle",
  "input": {"pokemonA": "Bulbasaur", "pokemonB": "Squirtle"}
}
```

**Tool output:**
```json
{"winner": "Squirtle", "turns": 12, "log": […]}
```

**Assistant (summary):**
"Squirtle wins after 12 turns. Highlights: Bulbasaur misses a Sleep Powder,
Squirtle lands a critical Water Gun, Bulbasaur faints from poison."

### Example 2
**User:** "Run Pikachu against Charmander at level 100 with seed 99."

**Assistant (tool call):**
```json
{
  "tool": "simulate_battle",
  "input": {
    "pokemonA": "Pikachu",
    "pokemonB": "Charmander",
    "level": 100,
    "seed": 99
  }
}
```

**Tool output:**
```json
{"winner": "Pikachu", "turns": 8, "log": […]}
```

**Assistant (summary):**
"Pikachu triumphs in 8 turns. Key moments: Charmander's Ember causes burn,
Pikachu counters with Thunderbolt, Charmander's HP drops to zero." 

If a Pokémon name is invalid, apologize, suggest two valid Pokémon (e.g.,
"Bulbasaur" or "Charmander"), and ask the user to resubmit.
