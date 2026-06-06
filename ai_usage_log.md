# AI Usage Log

## How AI was used in this project

### Code generation
- Claude (claude.ai) was used to generate the initial project scaffold, MCP server, CrewAI agent/task/crew files, and Streamlit dashboard
- All generated code was reviewed, tested, and understood before submission
- Bugs found during testing (context passing, task descriptions) were debugged and fixed with AI assistance

### Decision support
- Used Claude to think through agent role separation (Researcher vs Analyst vs Writer)
- Used Claude to review the MCP server for security risks (prompt injection, path traversal)
- Used Claude to draft task descriptions that enforce grounding

### Documentation
- decision_log.md, reflection.md, and README were drafted with AI assistance and then personalised
- All content reflects genuine understanding of the project

### What AI did NOT do
- AI did not run or test the code — that was done locally
- AI did not design the domain or data — e-commerce complaints domain was my choice
- AI did not explain the Week 14 rubric — I read and mapped that myself

### Verification
Every function in the MCP server (`search_documents`, `read_record`, `save_report`, `get_open_complaints`, `get_document_list`, `investigate_open_complaints`) and every agent in the crew can be explained line by line. The context-passing bug and its fix are described in reflection.md from personal experience running the system.

### Tools used
- Claude (Anthropic) — primary AI assistant for code and docs
- Ollama + llama3.2 — local LLM for running the crew
- CrewAI docs + FastMCP docs — primary references
