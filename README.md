# MCP + CrewAI E-Commerce Customer Complaints Investigation System

## Overview

This project uses CrewAI agents and an MCP (Model Context Protocol) server to automatically investigate unresolved customer complaints, identify product defects, and generate a management-ready report.

**Stack:**
- CrewAI Multi-Agent Framework
- MCP Server (FastMCP)
- Ollama (Llama 3.2) — runs locally, no API key needed
- Local Knowledge Base (policy docs + support tickets)
- CSV Complaints Data
- Automated Markdown Report Generation

---

## Business Problem

An e-commerce team wants to understand:
- Which customer complaints are still unresolved?
- Which products have recurring defects?
- What evidence supports each complaint?
- What actions should be taken?

Instead of manually reviewing documents, agents automatically analyse company records and generate an investigation report.

---

## Architecture

```
                +----------------+
                |   User Query   |
                +-------+--------+
                        |
                        v
                +----------------+
                |  CrewAI Crew   |
                +-------+--------+
                        |
        --------------------------------
        |               |              |
        v               v              v
+------------+  +-------------+  +------------+
| Researcher |  |   Analyst   |  |   Writer   |
+------------+  +-------------+  +------------+
        |               |              |
        --------------------------------
                        |
                        v
                +----------------+
                |   MCP Server   |
                +-------+--------+
                        |
          ---------------------------
          |            |            |
          v            v            v
   complaints.csv  Documents    Reports
```

---

## Agent Workflow

### Agent 1: Customer Complaints Researcher
- Calls `investigate_open_complaints()`
- Retrieves unresolved complaints
- Collects supporting policy and product documents
- Output: Grounded evidence report

### Agent 2: Customer Experience Analyst
- Analyses evidence
- Determines root causes (defects, shipping, etc.)
- Identifies impacted products
- Output: Structured operational analysis

### Agent 3: Report Writer
- Writes final management report
- Saves report via `save_report()` MCP tool
- Output: Markdown report in `outputs/reports/`

---

## MCP Tools

| Tool | Description |
|------|-------------|
| `investigate_open_complaints()` | Returns open complaints + evidence |
| `get_open_complaints()` | Returns all unresolved complaints |
| `get_document_list()` | Lists available policy/product docs |
| `search_documents(query)` | Keyword search across documents |
| `read_record(id)` | Read a document or complaint by ID |
| `save_report(title, content)` | Saves markdown report to disk |

---

## Dataset

**Documents (`data/docs/`):**
```
returns_policy.txt
refund_policy.txt
shipping_policy.txt
vendor_agreement.txt
warehouse_guidelines.txt
product_headphones.txt
product_usb_hub.txt
support_ticket_001.txt
support_ticket_002.txt
support_ticket_003.txt
```

**Complaints (`data/complaints.csv`):**
```csv
complaint_id,product,issue,status,created_date
2001,Wireless Headphones,Defective unit - no sound from left ear,Open,2026-05-10
...
```

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/avishkajindal05/ecommerce-crew.git
cd ecommerce-crew

# 2. Create virtual environment
python -m venv .venv
Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Start Ollama

```bash
ollama serve
ollama pull llama3.2
```

Verify:
```bash
ollama list
# Expected: llama3.2
```

---

## Run

```bash
python main.py
```

---

## Example Query

```
Which unresolved customer complaints are linked to product defects
and what evidence supports this conclusion?
```

---

## Example Output

```
Affected Complaints: 2001, 2004, 2007, 2008, 2009
Affected Products: Wireless Headphones, USB-C Hub, Laptop Stand

Evidence:
product_headphones.txt — Known batch defect WH200-B05 to B08
product_usb_hub.txt — Firmware defect causing overheating
support_ticket_001.txt — Confirmed defective headphone unit
support_ticket_002.txt — USB hub overheating complaint
vendor_agreement.txt — Vendor accountability clause triggered
```

---

## Run Tests

```bash
pytest tests/
```

---

## Future Enhancements

- Streamlit dashboard for complaint tracking
- Vector DB + RAG for semantic document search
- Real-time complaint ingestion via webhook
- Sentiment analysis on complaint text
- Automated vendor notification emails

---

## Technology Stack

- Python 3.11
- CrewAI
- MCP SDK (FastMCP)
- Ollama + Llama 3.2
- Pandas
- Markdown Reporting

---

## Author

Avishka Jindal
