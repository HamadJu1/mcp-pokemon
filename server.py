from __future__ import annotations

from mcp.server import Server

server = Server("mcp-pokemon")

# register resources and tools
import mcp.resources  # noqa: F401
import mcp.tools  # noqa: F401


if __name__ == "__main__":
    server.run()
