"""
Kali Linux integration tools.

Architecture: MCP server connects to Kali via SSH and runs allowed tools.
Kali should run as a VM or LXC container on Proxmox.

Security model:
  - Allowlist of permitted tools (set KALI_ALLOWED_TOOLS in .env)
  - All commands are logged with full args before execution
  - Targets are validated to prevent scope creep
  - SSH key auth only — no password auth

Setup steps:
  1. Deploy Kali as VM/LXC in Proxmox
  2. Create a dedicated user on Kali (not root): adduser mcp-runner
  3. Generate an SSH keypair on the MCP server: ssh-keygen -t ed25519 -f ~/.ssh/kali_id_ed25519
  4. Copy public key to Kali: ssh-copy-id -i ~/.ssh/kali_id_ed25519.pub mcp-runner@<kali-ip>
  5. Set KALI_HOST, KALI_USER, KALI_SSH_KEY_PATH in .env

Dependencies:
    pip install asyncssh
"""

import json
import logging
from mcp import types
from config import Config

# TODO: uncomment when asyncssh is installed
# import asyncssh

log = logging.getLogger("mcp-server.kali")

# These are the defaults; override via KALI_ALLOWED_TOOLS in .env
DEFAULT_ALLOWED_TOOLS = {
    "nmap", "nikto", "gobuster", "whatweb", "sslscan",
    "enum4linux", "dnsrecon", "subfinder", "httpx",
}

TOOLS: list[types.Tool] = [
    types.Tool(
        name="kali_run_tool",
        description=(
            "Run an allowed Kali Linux security tool against a target. "
            "Only tools in the configured allowlist will execute. "
            "Use only on systems you own or have explicit permission to test."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "tool": {
                    "type": "string",
                    "description": "Tool name, e.g. 'nmap', 'nikto', 'gobuster'.",
                },
                "target": {
                    "type": "string",
                    "description": "IP address or hostname to run the tool against.",
                },
                "flags": {
                    "type": "string",
                    "description": "Additional flags/arguments, e.g. '-sV -p 80,443'.",
                    "default": "",
                },
            },
            "required": ["tool", "target"],
        },
    ),
    types.Tool(
        name="kali_list_allowed_tools",
        description="List which Kali tools are permitted by this server's configuration.",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
]


async def handle(name: str, args: dict, config: Config) -> str:
    allowed = set(config.get("kali_allowed_tools", list(DEFAULT_ALLOWED_TOOLS)))

    if name == "kali_list_allowed_tools":
        return json.dumps(sorted(allowed), indent=2)

    if name == "kali_run_tool":
        return await _run_tool(args, config, allowed)

    raise ValueError(f"kali module cannot handle tool: {name}")


async def _run_tool(args: dict, config: Config, allowed: set[str]) -> str:
    tool = args["tool"].strip()
    target = args["target"].strip()
    flags = args.get("flags", "").strip()

    # Safety checks
    if tool not in allowed:
        return f"Error: '{tool}' is not in the allowed tools list: {sorted(allowed)}"
    if not target or any(c in target for c in [";", "&", "|", "`", "$", "\n"]):
        return "Error: Invalid target — shell metacharacters are not permitted."

    command = f"{tool} {flags} {target}".strip()
    log.warning(f"KALI EXEC | tool={tool} target={target} flags={flags!r}")

    # async with asyncssh.connect(
    #     config["kali_host"],
    #     username=config["kali_user"],
    #     client_keys=[config["kali_ssh_key_path"]],
    #     known_hosts=None,  # TODO: set up known_hosts properly in production
    # ) as conn:
    #     result = await conn.run(command, check=False, timeout=120)
    #     output = result.stdout or ""
    #     if result.stderr:
    #         output += f"\n[stderr]\n{result.stderr}"
    #     return output or "(no output)"

    raise NotImplementedError(
        "Install asyncssh, configure SSH key, and uncomment the implementation"
    )
