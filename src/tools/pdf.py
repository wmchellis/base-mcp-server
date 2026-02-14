"""
PDF integration tools.

Dependencies (add to requirements.txt when ready):
    pymupdf       — fast extraction, image rendering, annotation
    pdfplumber    — table extraction, layout-aware text
    pypdf         — form filling (AcroForms)
    reportlab     — generating new PDFs from scratch

Install:
    pip install pymupdf pdfplumber pypdf reportlab
"""

from mcp import types
from config import Config

# TODO: uncomment when dependencies are installed
# import fitz          # pymupdf
# import pdfplumber
# from pypdf import PdfReader, PdfWriter

TOOLS: list[types.Tool] = [
    types.Tool(
        name="pdf_read",
        description="Extract all text from a PDF file.",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute path to the PDF file."}
            },
            "required": ["path"],
        },
    ),
    types.Tool(
        name="pdf_extract_tables",
        description="Extract tables from a PDF and return them as JSON.",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "pages": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Page numbers (1-indexed). Omit for all pages.",
                },
            },
            "required": ["path"],
        },
    ),
    types.Tool(
        name="pdf_fill_form",
        description="Fill AcroForm fields in a PDF and save to a new file.",
        inputSchema={
            "type": "object",
            "properties": {
                "input_path": {"type": "string"},
                "output_path": {"type": "string"},
                "fields": {
                    "type": "object",
                    "description": "Dict of field_name -> value to fill.",
                },
            },
            "required": ["input_path", "output_path", "fields"],
        },
    ),
]


async def handle(name: str, args: dict, config: Config) -> str:
    if name == "pdf_read":
        return _pdf_read(args["path"])
    if name == "pdf_extract_tables":
        return _pdf_extract_tables(args["path"], args.get("pages"))
    if name == "pdf_fill_form":
        return _pdf_fill_form(args["input_path"], args["output_path"], args["fields"])
    raise ValueError(f"pdf module cannot handle tool: {name}")


def _pdf_read(path: str) -> str:
    # doc = fitz.open(path)
    # text = "\n\n".join(page.get_text() for page in doc)
    # return text
    raise NotImplementedError("Install pymupdf and uncomment the implementation")


def _pdf_extract_tables(path: str, pages: list[int] | None) -> str:
    # import json
    # with pdfplumber.open(path) as pdf:
    #     target_pages = [pdf.pages[i - 1] for i in pages] if pages else pdf.pages
    #     tables = [page.extract_tables() for page in target_pages]
    # return json.dumps(tables)
    raise NotImplementedError("Install pdfplumber and uncomment the implementation")


def _pdf_fill_form(input_path: str, output_path: str, fields: dict) -> str:
    # reader = PdfReader(input_path)
    # writer = PdfWriter()
    # writer.append(reader)
    # writer.update_page_form_field_values(writer.pages[0], fields)
    # with open(output_path, "wb") as f:
    #     writer.write(f)
    # return f"Form filled and saved to {output_path}"
    raise NotImplementedError("Install pypdf and uncomment the implementation")
