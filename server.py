"""
Base MCP Server
Entry point for the Model Context Protocol server.
"""

import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp import types

from config import load_config
from tools import get_all_tools, dispatch_tool

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/mcp-server.log"),
    ],
)
log = logging.getLogger("mcp-server")

# ── Server init ───────────────────────────────────────────────────────────────
server = Server("base-mcp-server")
config = load_config()


# ── Tool registration ─────────────────────────────────────────────────────────
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """Return all registered tools to the client."""
    tools = get_all_tools()
    log.info(f"Listing {len(tools)} tools")
    return tools


@server.call_tool()
async def call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Dispatch a tool call and return the result."""
    log.info(f"Tool called: {name} | args: {arguments}")
    try:
        result = await dispatch_tool(name, arguments or {}, config)
        log.info(f"Tool succeeded: {name}")
        return [types.TextContent(type="text", text=result)]
    except ValueError as e:
        log.warning(f"Tool not found: {name}")
        raise
    except Exception as e:
        log.error(f"Tool error [{name}]: {e}", exc_info=True)
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


# ── Run ───────────────────────────────────────────────────────────────────────
async def main():
    log.info("Starting base-mcp-server via stdio transport")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="base-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
