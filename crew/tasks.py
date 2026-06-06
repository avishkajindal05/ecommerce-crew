from crewai import Task


def research_task(agent, question):
    return Task(
        description="""
Call investigate_open_complaints.

Return:

1. Open complaint IDs
2. Products affected
3. Evidence documents

Use only returned evidence.
Do not invent document names.
""",
        expected_output="Grounded evidence report.",
        agent=agent
    )


def analysis_task(agent, context):
    return Task(
        description="""
        Analyze the complaint evidence.

        Determine:
        - unresolved complaints
        - root causes (defects, shipping, returns)
        - impacted products
        - supporting evidence
        """,
        expected_output="Structured analysis.",
        context=[context],
        agent=agent
    )


def report_task(agent, context):
    return Task(
        description="""
        Write a final report.

        Include:
        - findings
        - evidence
        - recommendations

        Do not invent information.
        """,
        expected_output="Final markdown report.",
        context=[context],
        agent=agent
    )


def save_task(agent, context):
    return Task(
        description="""
Use save_report tool.

Title:
Customer Complaints Investigation

Save the final report.
""",
        context=[context],
        agent=agent
    )
