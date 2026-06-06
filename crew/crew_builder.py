from crewai import Crew, Process

from crew.agents import (
    create_researcher,
    create_analyst,
    create_writer
)

from crew.tasks import (
    research_task,
    analysis_task,
    report_task
)


def build_crew(question, tools):

    researcher = create_researcher(tools)
    analyst = create_analyst(tools)
    writer = create_writer(tools)

    task1 = research_task(researcher, question)
    task2 = analysis_task(analyst, task1)
    task3 = report_task(writer, task2)

    return Crew(
        agents=[researcher, analyst, writer],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        verbose=True
    )
