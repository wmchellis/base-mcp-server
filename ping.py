"""
ping tool — sanity check that the server is alive.
Also serves as a copy-paste template for every new tool you add.

Pattern for every tool file:
  TOOLS  → list of mcp.types.Tool  (schema declarations)
  handle → async def(name, args, config) -> str
"""

import json
from datetime import datetime, timezone
from mcp import types
from config import Config


# ── Tool schemas (what Claude sees) ──────────────────────────────────────────
TOOLS: list[types.Tool] = [
    types.Tool(
        name="ping",
        description="Health check. Returns server status and timestamp.",
        inputSchema={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Optional message to echo back.",
                }
            },
            "required": [],
        },
    ),
    types.Tool(
        name="list_config_keys",
        description=(
            "List which integrations are configured (keys present, values redacted). "
            "Useful for verifying .env is loaded correctly."
        ),
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
]


# ── Handler ───────────────────────────────────────────────────────────────────
async def handle(name: str, args: dict, config: Config) -> str:
    if name == "ping":
        return _ping(args)
    if name == "list_config_keys":
        return _list_config_keys(config)
    raise ValueError(f"ping module cannot handle tool: {name}")


def _ping(args: dict) -> str:
    echo = args.get("message", "")
    payload = {
        "status": "ok",
        "server": "base-mcp-server",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if echo:
        payload["echo"] = echo
    return json.dumps(payload, indent=2)


def _list_config_keys(config: Config) -> str:
    summary = {}
    for key, value in config.items():
        if isinstance(value, list):
            summary[key] = f"[list, {len(value)} items]"
        elif isinstance(value, bool):
            summary[key] = str(value)
        elif value:
            summary[key] = "✓ set"
        else:
            summary[key] = "✗ not set"
    return json.dumps(summary, indent=2)
