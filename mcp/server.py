from __future__ import annotations

from typing import Any, Callable, Dict


class Server:
    def __init__(self, name: str):
        self.name = name
        self.resources: Dict[str, Any] = {}
        self.tools: Dict[str, Callable] = {}

    def resource(self, name: str):
        def decorator(cls):
            self.resources[name] = cls()
            return cls
        return decorator

    def tool(self, name: str):
        def decorator(func):
            self.tools[name] = func
            return func
        return decorator

    def run(self) -> None:
        pass

    def create_mcp_config(self) -> Dict[str, Any]:
        return {"resources": list(self.resources.keys()), "tools": list(self.tools.keys())}


class Resource:
    pass


class Tool:
    pass
