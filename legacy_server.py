from __future__ import annotations

from pokemon_mcp.server import Server

server = Server("mcp-pokemon")

# register resources and tools
import pokemon_mcp.resources  # noqa: F401
import pokemon_mcp.tools  # noqa: F401


if __name__ == "__main__":
    server.run()
