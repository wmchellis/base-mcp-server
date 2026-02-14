"""
Proxmox VE integration tools.

Auth strategy: API Token (recommended over username/password).

Setup steps:
  1. In Proxmox UI → Datacenter → Permissions → API Tokens
  2. Create a token for a dedicated user (e.g. mcp@pam)
  3. Grant the user only the permissions it needs (PVEVMAdmin, PVEAuditor, etc.)
  4. Set PROXMOX_HOST, PROXMOX_USER, PROXMOX_TOKEN_NAME, PROXMOX_TOKEN_VALUE in .env

Dependencies:
    pip install proxmoxer requests
"""

import json
from mcp import types
from config import Config

# TODO: uncomment when proxmoxer is installed
# from proxmoxer import ProxmoxAPI

TOOLS: list[types.Tool] = [
    types.Tool(
        name="proxmox_list_nodes",
        description="List all nodes in the Proxmox cluster with their status.",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    types.Tool(
        name="proxmox_list_vms",
        description="List all VMs and LXC containers across all nodes.",
        inputSchema={
            "type": "object",
            "properties": {
                "node": {"type": "string", "description": "Filter to a specific node name."}
            },
            "required": [],
        },
    ),
    types.Tool(
        name="proxmox_vm_status",
        description="Get detailed status of a specific VM or container.",
        inputSchema={
            "type": "object",
            "properties": {
                "node": {"type": "string"},
                "vmid": {"type": "integer"},
                "type": {"type": "string", "enum": ["qemu", "lxc"], "default": "qemu"},
            },
            "required": ["node", "vmid"],
        },
    ),
    types.Tool(
        name="proxmox_vm_power",
        description="Start, stop, or reboot a VM or container.",
        inputSchema={
            "type": "object",
            "properties": {
                "node": {"type": "string"},
                "vmid": {"type": "integer"},
                "action": {"type": "string", "enum": ["start", "stop", "reboot", "shutdown"]},
                "type": {"type": "string", "enum": ["qemu", "lxc"], "default": "qemu"},
            },
            "required": ["node", "vmid", "action"],
        },
    ),
    types.Tool(
        name="proxmox_create_snapshot",
        description="Create a snapshot of a VM.",
        inputSchema={
            "type": "object",
            "properties": {
                "node": {"type": "string"},
                "vmid": {"type": "integer"},
                "snapname": {"type": "string", "description": "Snapshot name (no spaces)."},
                "description": {"type": "string"},
            },
            "required": ["node", "vmid", "snapname"],
        },
    ),
]


def _get_proxmox(config: Config):
    # return ProxmoxAPI(
    #     config["proxmox_host"],
    #     user=config["proxmox_user"],
    #     token_name=config["proxmox_token_name"],
    #     token_value=config["proxmox_token_value"],
    #     verify_ssl=config["proxmox_verify_ssl"],
    # )
    raise NotImplementedError("Install proxmoxer and configure credentials")


async def handle(name: str, args: dict, config: Config) -> str:
    # px = _get_proxmox(config)

    if name == "proxmox_list_nodes":
        # nodes = px.nodes.get()
        # return json.dumps(nodes, indent=2)
        raise NotImplementedError

    if name == "proxmox_list_vms":
        # node_filter = args.get("node")
        # nodes = [px.nodes(node_filter)] if node_filter else [px.nodes(n["node"]) for n in px.nodes.get()]
        # vms = []
        # for node in nodes:
        #     vms.extend(node.qemu.get())
        #     vms.extend(node.lxc.get())
        # return json.dumps(vms, indent=2)
        raise NotImplementedError

    if name == "proxmox_vm_status":
        # vm_type = args.get("type", "qemu")
        # endpoint = px.nodes(args["node"]).qemu if vm_type == "qemu" else px.nodes(args["node"]).lxc
        # status = endpoint(args["vmid"]).status.current.get()
        # return json.dumps(status, indent=2)
        raise NotImplementedError

    if name == "proxmox_vm_power":
        # vm_type = args.get("type", "qemu")
        # endpoint = px.nodes(args["node"]).qemu if vm_type == "qemu" else px.nodes(args["node"]).lxc
        # endpoint(args["vmid"]).status(args["action"]).post()
        # return f"Action '{args['action']}' sent to VMID {args['vmid']}"
        raise NotImplementedError

    if name == "proxmox_create_snapshot":
        # px.nodes(args["node"]).qemu(args["vmid"]).snapshot.post(
        #     snapname=args["snapname"],
        #     description=args.get("description", ""),
        # )
        # return f"Snapshot '{args['snapname']}' created for VMID {args['vmid']}"
        raise NotImplementedError

    raise ValueError(f"proxmox module cannot handle tool: {name}")
