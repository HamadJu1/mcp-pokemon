# Smoke Test Checklist

Use this checklist to verify the battle simulator MCP integration.

1. **Tool discovery**  
   Run `mcp dev server.py` and confirm `simulate_battle` appears under the
   reported Tools.
2. **Direct invocation**  
   Send a request with the payload
   `{ "pokemonA": "Bulbasaur", "pokemonB": "Squirtle" }` to
   `simulate_battle` and verify JSON output with keys `winner`, `turns` and `log`.
3. **Prompt Tab behaviour**  
   In an MCP client, ask "Simulate Bulbasaur vs Squirtle" and ensure the
   assistant issues a `simulate_battle` tool call rather than a fabricated
   answer. The summary should mention the winner, number of turns, and a few
   highlights.

The default parameters keep runtime below two seconds; investigate if responses
are noticeably slower.
