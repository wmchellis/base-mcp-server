"""
Google Drive integration tools.

Uses a Service Account for server-side auth (no browser flow required).

Setup steps:
  1. Go to console.cloud.google.com → New Project
  2. Enable the Google Drive API
  3. Create a Service Account → download JSON key
  4. Set GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/key.json in config/.env
  5. Share any Drive folders with the service account email address

Dependencies:
    pip install google-api-python-client google-auth
"""

import json
from mcp import types
from config import Config

# TODO: uncomment when dependencies are installed
# from googleapiclient.discovery import build
# from google.oauth2 import service_account

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    # Add drive (read/write) scope only when needed:
    # "https://www.googleapis.com/auth/drive",
]

TOOLS: list[types.Tool] = [
    types.Tool(
        name="gdrive_list_files",
        description="List files in a Google Drive folder.",
        inputSchema={
            "type": "object",
            "properties": {
                "folder_id": {
                    "type": "string",
                    "description": "Drive folder ID. Omit to use root.",
                },
                "query": {
                    "type": "string",
                    "description": "Optional Drive query string, e.g. \"name contains 'report'\"",
                },
                "max_results": {"type": "integer", "default": 20},
            },
            "required": [],
        },
    ),
    types.Tool(
        name="gdrive_read_file",
        description="Read the text content of a Google Doc or plain text file from Drive.",
        inputSchema={
            "type": "object",
            "properties": {
                "file_id": {"type": "string", "description": "Google Drive file ID."}
            },
            "required": ["file_id"],
        },
    ),
    types.Tool(
        name="gdrive_upload_file",
        description="Upload a local file to Google Drive.",
        inputSchema={
            "type": "object",
            "properties": {
                "local_path": {"type": "string"},
                "drive_filename": {"type": "string"},
                "folder_id": {"type": "string", "description": "Destination folder ID."},
            },
            "required": ["local_path", "drive_filename"],
        },
    ),
]


def _build_service(config: Config):
    # creds = service_account.Credentials.from_service_account_file(
    #     config["google_service_account_json"], scopes=SCOPES
    # )
    # return build("drive", "v3", credentials=creds)
    raise NotImplementedError("Install google-api-python-client and configure service account")


async def handle(name: str, args: dict, config: Config) -> str:
    if name == "gdrive_list_files":
        return _list_files(args, config)
    if name == "gdrive_read_file":
        return _read_file(args["file_id"], config)
    if name == "gdrive_upload_file":
        return _upload_file(args, config)
    raise ValueError(f"gdrive module cannot handle tool: {name}")


def _list_files(args: dict, config: Config) -> str:
    # service = _build_service(config)
    # q = f"'{args.get('folder_id', 'root')}' in parents"
    # if args.get("query"):
    #     q += f" and {args['query']}"
    # results = service.files().list(q=q, pageSize=args.get("max_results", 20),
    #                                fields="files(id, name, mimeType, modifiedTime)").execute()
    # return json.dumps(results.get("files", []), indent=2)
    raise NotImplementedError("Implement after setting up Service Account")


def _read_file(file_id: str, config: Config) -> str:
    # service = _build_service(config)
    # # Export Google Docs as plain text; download others directly
    # try:
    #     content = service.files().export(fileId=file_id, mimeType="text/plain").execute()
    #     return content.decode("utf-8")
    # except Exception:
    #     content = service.files().get_media(fileId=file_id).execute()
    #     return content.decode("utf-8", errors="replace")
    raise NotImplementedError("Implement after setting up Service Account")


def _upload_file(args: dict, config: Config) -> str:
    # from googleapiclient.http import MediaFileUpload
    # service = _build_service(config)
    # meta = {"name": args["drive_filename"]}
    # if args.get("folder_id"):
    #     meta["parents"] = [args["folder_id"]]
    # media = MediaFileUpload(args["local_path"])
    # f = service.files().create(body=meta, media_body=media, fields="id").execute()
    # return f"Uploaded. File ID: {f['id']}"
    raise NotImplementedError("Implement after setting up Service Account")
