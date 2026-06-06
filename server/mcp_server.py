"""
MCP Server — E-Commerce Operations Assistant
Tools: search_documents, read_record, save_report,
       get_open_complaints, get_document_list, investigate_open_complaints
"""

from pathlib import Path
from datetime import datetime
from typing import Annotated
import re
import pandas as pd
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent
DOCS_DIR   = BASE_DIR / "data" / "docs"
CSV_FILE   = BASE_DIR / "data" / "complaints.csv"
REPORT_DIR = BASE_DIR / "outputs" / "reports"
TRACE_DIR  = BASE_DIR / "outputs" / "traces"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
TRACE_DIR.mkdir(parents=True, exist_ok=True)

mcp = FastMCP("EcommerceAssistant")

# ── Input schemas (strict validation) ────────────────────────────────────────

class SearchInput(BaseModel):
    query: Annotated[str, Field(min_length=1, max_length=200)]

    @field_validator("query")
    @classmethod
    def sanitize(cls, v):
        # Strip anything that looks like a prompt injection
        if any(kw in v.lower() for kw in ["ignore previous", "system:", "forget", "jailbreak"]):
            raise ValueError("Query contains disallowed content.")
        return v.strip()

class RecordInput(BaseModel):
    record_id: Annotated[str, Field(min_length=1, max_length=100)]

    @field_validator("record_id")
    @classmethod
    def safe_id(cls, v):
        # Allow only alphanumeric, hyphens, underscores, dots
        if not re.match(r'^[\w\-\.]+$', v):
            raise ValueError(f"Invalid record_id '{v}'. Use only letters, digits, _ - .")
        return v.strip()

class ReportInput(BaseModel):
    title:   Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=1, max_length=100_000)]

    @field_validator("title")
    @classmethod
    def safe_title(cls, v):
        if not re.match(r'^[\w\s\-\.]+$', v):
            raise ValueError("Title contains disallowed characters.")
        return v.strip()


# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def search_documents(query: str) -> list:
    """
    Search policy and product documents by keyword.
    Returns list of {document, preview} dicts, or [] if nothing found.
    """
    try:
        inp = SearchInput(query=query)
    except Exception as e:
        return [{"error": str(e)}]

    q = inp.query.lower()
    results = []
    for file in sorted(DOCS_DIR.glob("*.txt")):
        content = file.read_text(encoding="utf-8")
        if q in content.lower():
            results.append({"document": file.name, "preview": content[:400]})
    return results


@mcp.tool()
def read_record(record_id: str) -> dict:
    """
    Read a document (by filename) or a complaint (by numeric ID).
    Returns the full content or an error message.
    """
    try:
        inp = RecordInput(record_id=record_id)
    except Exception as e:
        return {"error": str(e)}

    rid = inp.record_id

    # Try as a document file first
    doc_file = DOCS_DIR / rid
    if doc_file.exists() and doc_file.suffix == ".txt":
        return {"type": "document", "name": doc_file.name,
                "content": doc_file.read_text(encoding="utf-8")}

    # Try as a numeric complaint ID
    try:
        complaint_id = int(rid)
        df = pd.read_csv(CSV_FILE)
        row = df[df["complaint_id"] == complaint_id]
        if not row.empty:
            return {"type": "complaint", "data": row.iloc[0].to_dict()}
    except (ValueError, FileNotFoundError):
        pass

    return {"error": f"No document or complaint found for id '{rid}'."}


@mcp.tool()
def save_report(title: str, content: str) -> dict:
    """
    Save a markdown investigation report to outputs/reports/.
    Returns {status, file} on success or {error} on failure.
    """
    try:
        inp = ReportInput(title=title, content=content)
    except Exception as e:
        return {"error": str(e)}

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = re.sub(r'\s+', '_', inp.title)
    filename = REPORT_DIR / f"{timestamp}_{safe_title}.md"
    filename.write_text(inp.content, encoding="utf-8")
    return {"status": "saved", "file": str(filename)}


@mcp.tool()
def get_open_complaints() -> list:
    """Return all complaints with status == 'Open' as a list of dicts."""
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return [{"error": f"CSV not found at {CSV_FILE}"}]
    return df[df["status"] == "Open"].to_dict(orient="records")


@mcp.tool()
def get_document_list() -> list:
    """List all available document filenames in data/docs/."""
    return sorted(f.name for f in DOCS_DIR.glob("*.txt"))


@mcp.tool()
def investigate_open_complaints() -> dict:
    """
    Core investigation tool.
    Returns all open complaints + every evidence document that mentions
    defect, damaged, return, refund, or complaint.
    """
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return {"error": f"CSV not found at {CSV_FILE}"}

    open_complaints = df[df["status"] == "Open"].to_dict(orient="records")
    keywords = ["defect", "damaged", "return", "refund", "complaint", "overheating", "broken"]

    evidence = []
    for f in sorted(DOCS_DIR.glob("*.txt")):
        text = f.read_text(encoding="utf-8")
        if any(kw in text.lower() for kw in keywords):
            evidence.append({"document": f.name, "content": text})

    return {"complaints": open_complaints, "evidence": evidence}


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()
