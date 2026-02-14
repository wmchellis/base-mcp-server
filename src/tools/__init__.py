"""
Tool registry and dispatcher.

To add a new integration:
  1. Create src/tools/my_integration.py
  2. Implement TOOLS (list[types.Tool]) and handle(name, args, config) -> str
  3. Import and register it below — nothing else to change.
"""

from mcp import types
from config import Config

# ── Import tool modules ───────────────────────────────────────────────────────
from tools.ping import TOOLS as PING_TOOLS, handle as ping_handle

# Stubs — uncomment as you build each integration:
# from tools.pdf        import TOOLS as PDF_TOOLS,    handle as pdf_handle
# from tools.gdrive     import TOOLS as GDRIVE_TOOLS,  handle as gdrive_handle
# from tools.proxmox    import TOOLS as PROXMOX_TOOLS, handle as proxmox_handle
# from tools.kali       import TOOLS as KALI_TOOLS,    handle as kali_handle

# ── Registry ──────────────────────────────────────────────────────────────────
# Each entry: (list_of_tools, handler_coroutine)
_REGISTRY = [
    (PING_TOOLS, ping_handle),
    # (PDF_TOOLS,    pdf_handle),
    # (GDRIVE_TOOLS,  gdrive_handle),
    # (PROXMOX_TOOLS, proxmox_handle),
    # (KALI_TOOLS,    kali_handle),
]

# Build a flat name → handler map at import time
_DISPATCH: dict[str, object] = {}
for tool_list, handler in _REGISTRY:
    for tool in tool_list:
        _DISPATCH[tool.name] = handler


def get_all_tools() -> list[types.Tool]:
    """Return every registered tool (called by server.list_tools)."""
    tools = []
    for tool_list, _ in _REGISTRY:
        tools.extend(tool_list)
    return tools


async def dispatch_tool(name: str, args: dict, config: Config) -> str:
    """Route a tool call to the correct handler."""
    handler = _DISPATCH.get(name)
    if handler is None:
        raise ValueError(f"Unknown tool: '{name}'")
    return await handler(name, args, config)
