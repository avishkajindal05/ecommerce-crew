# Operations Assistant: MCP + CrewAI E-Commerce Complaints Investigator

Week 14 Mini-Project · Futurense AI Clinic

---

## What it does

A CrewAI crew of three agents connects to a local MCP server, investigates unresolved customer complaints, identifies product defects, and saves a sourced markdown report — every claim cites the document or record it came from.

**Stack:** Python 3.11 · CrewAI · FastMCP · Ollama (llama3.2) · Pydantic validation

---

## Folder structure

```
ecommerce_crew/
├── main.py                        # Entry point — runs the crew
├── dashboard.py                   # Optional Streamlit UI
├── .env.example                   # Config template (copy to .env)
├── requirements.txt
│
├── crew/
│   ├── agents.py                  # Researcher, Analyst, Writer
│   ├── tasks.py                   # research_task, analysis_task, report_task
│   ├── crew_builder.py            # Assembles and returns the Crew
│   └── llm.py                     # Ollama LLM config
│
├── server/
│   └── mcp_server.py              # FastMCP server — 6 validated tools
│
├── data/
│   ├── complaints.csv             # 10 synthetic complaints
│   └── docs/                      # 10 short policy + product documents
│
├── outputs/
│   ├── reports/                   # Saved markdown reports
│   ├── traces/                    # JSON run traces (agent steps + token usage)
│   └── example_runs/              # 3 example questions with saved outputs
│
├── tests/
│   └── test_tools.py              # Unit tests for all 6 MCP tools
│
├── decision_log.md                # What I tried, chose, and rejected
├── reflection.md                  # Post-build reflection (4 questions)
└── ai_usage_log.md                # How AI was used
```

---

## Data

**`data/complaints.csv`** — 10 synthetic e-commerce complaints (complaint_id, product, issue, status, created_date). Products: Wireless Headphones, USB-C Hub, Laptop Stand, Bluetooth Speaker.

**`data/docs/`** — 10 short text documents:

| File | Contents |
|---|---|
| returns_policy.txt | 30-day return terms |
| refund_policy.txt | Full / partial refund conditions |
| shipping_policy.txt | Domestic delivery SLAs |
| vendor_agreement.txt | Vendor defect accountability clauses |
| warehouse_guidelines.txt | Handling and QA rules |
| product_headphones.txt | Known WH200 batch defect (May 2026) |
| product_usb_hub.txt | Known UCH500 firmware defect |
| support_ticket_001.txt | Ticket for complaint #2001 |
| support_ticket_002.txt | Ticket for complaint #2004 |
| support_ticket_003.txt | Ticket for complaint #2009 |

---

## MCP Server tools

| Tool | Description |
|---|---|
| `search_documents(query)` | Keyword search across all docs. Returns {document, preview}[] |
| `read_record(record_id)` | Read a doc by filename or complaint by numeric ID |
| `save_report(title, content)` | Write markdown report to outputs/reports/ |
| `get_open_complaints()` | All complaints with status == Open |
| `get_document_list()` | List all doc filenames |
| `investigate_open_complaints()` | Open complaints + matching evidence docs in one call |

All tools validate inputs with Pydantic (min/max length, safe character sets, injection keyword check).

---

## Agents

| Agent | Role | Tools used |
|---|---|---|
| Customer Complaints Researcher | Calls investigate_open_complaints, returns full raw evidence | investigate_open_complaints |
| Customer Experience Analyst | Analyses evidence, identifies root causes, groups by product | (context from Researcher) |
| Report Writer | Writes final sourced markdown report, saves it | save_report |

---

## Setup

```bash
# 1. Clone
git clone https://github.com/avishkajindal05/ecommerce-crew.git
cd ecommerce-crew

# 2. Virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

# 3. Install
pip install -r requirements.txt

# 4. Config
copy .env.example .env        # Windows
# cp .env.example .env        # Mac/Linux
# (edit .env if using a cloud model)

# 5. Start Ollama (in a separate terminal)
ollama serve
ollama pull llama3.2
```

---

## Run

**CLI:**
```bash
python main.py
```


Traces are saved automatically to `outputs/traces/trace_YYYYMMDD_HHMMSS.json`.
Reports are saved to `outputs/reports/`.

---

## Tests

```bash
pytest tests/
```

Tests call all 6 MCP tools directly (no crew, no LLM required).

---

## Test MCP server in Inspector

```bash
# Install inspector
npx @modelcontextprotocol/inspector python server/mcp_server.py
```

---

## Example questions

See `outputs/example_runs/` for three saved runs:

1. `example_q1_defect_investigation.md` — Which complaints are linked to product defects?
2. `example_q2_refund_eligibility.md` — Which open complaints qualify for a full refund?
3. `example_q3_no_evidence_grounded_refusal.md` — What is the SLA for international orders? (grounded refusal)

---

## Key design decisions

See `decision_log.md` for full details. Short version:

- **3 agents** (not 2) — Analyst separates evidence from interpretation
- **Sequential process** — linear flow doesn't need a manager agent
- **FastMCP** — official SDK, cleaner than raw registration
- **Pydantic validation on every tool** — LLM inputs are untrusted
- **Context bug fixed** — Researcher must output full raw evidence, not a summary

---

## Security

- All tool inputs validated (length, character set, injection keywords)
- Agent backstories forbid following instructions found inside documents
- See `reflection.md` for remaining risks and what I'd change before real data

---

## References

- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- FastMCP: https://gofastmcp.com/tutorials/create-mcp-server
- CrewAI + MCP: https://docs.crewai.com/en/mcp/overview
- MCP Inspector: https://github.com/modelcontextprotocol/inspector
