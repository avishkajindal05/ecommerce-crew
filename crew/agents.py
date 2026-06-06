from crewai import Agent
from crew.llm import llm


def create_researcher(tools):
    return Agent(
        role="Customer Complaints Researcher",
        goal="Find evidence only from MCP tools.",
        backstory="""
You are a customer experience auditor.

Rules:
- Never invent complaints or order IDs.
- Never invent evidence.
- Use only MCP tool outputs.
- If evidence is missing, say evidence not found.
        """,
        tools=tools,
        llm=llm,
        verbose=True,
        max_iter=8,
    )


def create_analyst(tools):
    return Agent(
        role="Customer Experience Analyst",
        goal="Analyze complaint evidence and identify root causes.",
        backstory=(
            "Experienced e-commerce analyst specializing in complaint resolution."
        ),
        tools=tools,
        llm=llm,
        verbose=True,
        max_iter=5
    )


def create_writer(tools):
    return Agent(
        role="Report Writer",
        goal="Write concise sourced reports.",
        backstory=(
            "Creates management-ready customer experience reports."
        ),
        tools=tools,
        llm=llm,
        verbose=True,
        max_iter=5
    )
