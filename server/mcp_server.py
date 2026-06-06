from pathlib import Path
from datetime import datetime
import pandas as pd

from mcp.server.fastmcp import FastMCP

# --------------------------------------------------
# Configuration
# --------------------------------------------------

DOCS_DIR = Path("data/docs")
CSV_FILE = Path("data/complaints.csv")
REPORT_DIR = Path("outputs/reports")

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# MCP Server
# --------------------------------------------------

mcp = FastMCP("EcommerceAssistant")

# --------------------------------------------------
# Tool 1 — Search documents
# --------------------------------------------------

@mcp.tool()
def search_documents(query: str):
    """Search policy and product documents."""
    query = str(query).lower()
    results = []
    for file in DOCS_DIR.glob("*.txt"):
        content = file.read_text(encoding="utf-8")
        if query in content.lower():
            results.append({
                "document": file.name,
                "preview": content[:300]
            })
    return results


# --------------------------------------------------
# Tool 2 — Read a document or complaint record
# --------------------------------------------------

@mcp.tool()
def read_record(record_id: str) -> dict:
    """Read a document or complaint by ID."""

    doc_file = DOCS_DIR / record_id
    if doc_file.exists():
        return {
            "type": "document",
            "name": doc_file.name,
            "content": doc_file.read_text(encoding="utf-8")
        }

    try:
        df = pd.read_csv(CSV_FILE)
        complaint_id = int(record_id)
        row = df[df["complaint_id"] == complaint_id]
        if not row.empty:
            return {
                "type": "complaint",
                "data": row.iloc[0].to_dict()
            }
    except Exception:
        pass

    return {"error": f"{record_id} not found"}


# --------------------------------------------------
# Tool 3 — Save report
# --------------------------------------------------

@mcp.tool()
def save_report(title: str, content: str) -> dict:
    """Save a markdown report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = REPORT_DIR / f"{timestamp}_{title.replace(' ', '_')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return {"status": "saved", "file": str(filename)}


# --------------------------------------------------
# Tool 4 — Get open complaints
# --------------------------------------------------

@mcp.tool()
def get_open_complaints():
    """Return all unresolved complaints."""
    df = pd.read_csv(CSV_FILE)
    open_complaints = df[df["status"] == "Open"]
    return open_complaints.to_dict(orient="records")


# --------------------------------------------------
# Tool 5 — Get document list
# --------------------------------------------------

@mcp.tool()
def get_document_list():
    """List all available documents."""
    return [f.name for f in DOCS_DIR.glob("*.txt")]


# --------------------------------------------------
# Tool 6 — Investigate open complaints
# --------------------------------------------------

@mcp.tool()
def investigate_open_complaints():
    """Return open complaints with supporting evidence documents."""
    df = pd.read_csv(CSV_FILE)
    open_complaints = df[df["status"] == "Open"]

    evidence = []
    for file in DOCS_DIR.glob("*.txt"):
        text = file.read_text(encoding="utf-8")
        if any(
            keyword in text.lower()
            for keyword in ["defect", "damaged", "return", "refund", "complaint"]
        ):
            evidence.append({
                "document": file.name,
                "content": text
            })

    return {
        "complaints": open_complaints.to_dict(orient="records"),
        "evidence": evidence
    }


# --------------------------------------------------
# Run server
# --------------------------------------------------

if __name__ == "__main__":
    mcp.run()
