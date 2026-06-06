from mcp import StdioServerParameters
from crewai_tools import MCPServerAdapter

from crew.crew_builder import build_crew


QUESTION = """
Which unresolved customer complaints are linked to product defects
and what evidence supports this conclusion?
"""


def main():

    server_params = StdioServerParameters(
        command="python",
        args=["server/mcp_server.py"]
    )

    with MCPServerAdapter(server_params) as tools:

        print("\nLoaded MCP Tools:")
        for tool in tools:
            print("-", tool.name)

        crew = build_crew(QUESTION, tools)
        result = crew.kickoff()

        print("\n")
        print("=" * 80)
        print(result)
        print("=" * 80)


if __name__ == "__main__":
    main()
