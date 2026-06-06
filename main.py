"""
Entry point — runs the CrewAI crew against the MCP server.
Saves a trace of every agent step and tool call to outputs/traces/.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

from mcp import StdioServerParameters
from crewai_tools import MCPServerAdapter
from crew.crew_builder import build_crew

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).parent
TRACE_DIR = BASE_DIR / "outputs" / "traces"
TRACE_DIR.mkdir(parents=True, exist_ok=True)

# ── Question (override via env var for Streamlit / tests) ─────────────────────
QUESTION = os.environ.get(
    "INVESTIGATION_QUESTION",
    "Which unresolved customer complaints are linked to product defects "
    "and what evidence supports this conclusion?"
)


def main():
    server_params = StdioServerParameters(
        command="python",
        args=[str(BASE_DIR / "server" / "mcp_server.py")]
    )

    with MCPServerAdapter(server_params) as tools:
        print("\n── MCP Tools loaded ──")
        for t in tools:
            print(f"  • {t.name}")

        crew = build_crew(QUESTION, tools)

        # Run and capture result
        result = crew.kickoff()

        # ── Save trace ────────────────────────────────────────────────────────
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_file = TRACE_DIR / f"trace_{timestamp}.json"

        trace_data = {
            "timestamp": timestamp,
            "question":  QUESTION,
            "result":    str(result),
            "usage":     result.token_usage.__dict__ if hasattr(result, "token_usage") else {},
        }

        # Include per-task outputs if available
        if hasattr(result, "tasks_output"):
            trace_data["tasks"] = [
                {
                    "agent":       t.agent,
                    "description": t.description[:120],
                    "output":      str(t.raw)[:2000],
                }
                for t in result.tasks_output
            ]

        trace_file.write_text(json.dumps(trace_data, indent=2), encoding="utf-8")
        print(f"\n── Trace saved → {trace_file.name}")

        # ── Print result ──────────────────────────────────────────────────────
        print("\n" + "=" * 80)
        print(result)
        print("=" * 80)


if __name__ == "__main__":
    main()
