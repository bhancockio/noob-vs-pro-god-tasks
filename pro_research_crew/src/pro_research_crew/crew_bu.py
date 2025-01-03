import os

import agentops
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

from pro_research_crew.tools.reddit_tavily_search import RedditTavilySearchTool
from pro_research_crew.tools.tavily_search_tool import TavilySearchTool


@CrewBase
class ProResearchCrew:
    """ProResearchCrew crew"""

    agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), skip_auto_end_session=True)

    # Learn more about YAML configuration files here:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[
                SerperDevTool(),
                TavilySearchTool(),
                RedditTavilySearchTool(),
            ],
            verbose=True,
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],
            verbose=True,
        )

    @task
    def serper_comparison_task(self) -> Task:
        return Task(
            config=self.tasks_config["serper_comparison_task"],
        )

    @task
    def tavily_comparison_task(self) -> Task:
        return Task(
            config=self.tasks_config["tavily_comparison_task"],
        )

    @task
    def reddit_search_comparison_task(self) -> Task:
        return Task(
            config=self.tasks_config["reddit_search_comparison_task"],
        )

    @task
    def final_comparison_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["final_comparison_report_task"],
            output_file="report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ProResearchCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
