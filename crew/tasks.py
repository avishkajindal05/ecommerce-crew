from crewai import Task


def research_task(agent, question):
    return Task(
        description="""
Call investigate_open_complaints tool now.

You MUST include in your output:
1. Every open complaint ID and its issue
2. Every product affected
3. Full content of every evidence document returned

Do not summarise. Return everything the tool gave you.
Do not invent anything.
""",
        expected_output=(
            "Complete list of open complaints with IDs, products, issues, "
            "and full text of all evidence documents."
        ),
        agent=agent
    )


def analysis_task(agent, context):
    return Task(
        description="""
Using ONLY the complaint data and evidence passed from the previous task:

1. List every unresolved complaint with its ID and product
2. Identify root causes (defect, shipping damage, firmware, etc.)
3. Group complaints by product
4. Match each complaint to supporting evidence documents
5. Note which products have multiple complaints (pattern = systemic issue)

Do not invent any complaint IDs or document names.
""",
        expected_output=(
            "Structured analysis: complaints grouped by product, "
            "root causes identified, evidence matched."
        ),
        context=[context],
        agent=agent
    )


def report_task(agent, context):
    return Task(
        description="""
Write a final markdown investigation report using ONLY the analysis passed from the previous task.

Structure:
## Final Report: Customer Complaints Investigation

## Executive Summary
(2-3 sentences)

## Open Complaints
(table: ID | Product | Issue | Root Cause)

## Findings
(key patterns and defects found)

## Evidence
(which documents support which findings)

## Recommendations
(concrete next steps per product)

Do not invent information. Use only what was passed to you.
""",
        expected_output="Complete markdown investigation report with all sections.",
        context=[context],
        agent=agent
    )
