"""
Config loader.
Reads .env file and exposes a typed config dict.
Add new integration keys here as you build them out.
"""

import os
from pathlib import Path
from typing import TypedDict

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / "config" / ".env")
except ImportError:
    pass  # dotenv optional; env vars can be set via systemd or shell


class Config(TypedDict, total=False):
    # Google Drive
    google_service_account_json: str
    google_drive_root_folder: str

    # Proxmox
    proxmox_host: str
    proxmox_user: str
    proxmox_token_name: str
    proxmox_token_value: str
    proxmox_verify_ssl: bool

    # Kali (SSH target)
    kali_host: str
    kali_user: str
    kali_ssh_key_path: str
    kali_allowed_tools: list[str]

    # Server
    log_level: str


def load_config() -> Config:
    cfg: Config = {
        # Google Drive
        "google_service_account_json": os.getenv(
            "GOOGLE_SERVICE_ACCOUNT_JSON", ""
        ),
        "google_drive_root_folder": os.getenv("GOOGLE_DRIVE_ROOT_FOLDER", ""),

        # Proxmox
        "proxmox_host": os.getenv("PROXMOX_HOST", ""),
        "proxmox_user": os.getenv("PROXMOX_USER", "mcp@pam"),
        "proxmox_token_name": os.getenv("PROXMOX_TOKEN_NAME", ""),
        "proxmox_token_value": os.getenv("PROXMOX_TOKEN_VALUE", ""),
        "proxmox_verify_ssl": os.getenv("PROXMOX_VERIFY_SSL", "true").lower() == "true",

        # Kali
        "kali_host": os.getenv("KALI_HOST", ""),
        "kali_user": os.getenv("KALI_USER", "kali"),
        "kali_ssh_key_path": os.getenv("KALI_SSH_KEY_PATH", "~/.ssh/kali_id_ed25519"),
        "kali_allowed_tools": os.getenv(
            "KALI_ALLOWED_TOOLS", "nmap,nikto,gobuster,whatweb,sslscan"
        ).split(","),

        # Server
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }
    return cfg
