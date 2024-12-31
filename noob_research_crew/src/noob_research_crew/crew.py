from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FirecrawlScrapeWebsiteTool, SerperDevTool

from noob_research_crew.tools.tavily_search_tool import TavilySearchTool
from noob_research_crew.tools.youtube_search_tool import (
    YoutubeVideoSearchAndDetailsTool,
)


@CrewBase
class NoobResearchCrew:
    """NoobResearchCrew crew"""

    # YAML Configurations
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[
                SerperDevTool(),
                TavilySearchTool(),
                FirecrawlScrapeWebsiteTool(),
                YoutubeVideoSearchAndDetailsTool(),
            ],
            verbose=True,
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(config=self.agents_config["reporting_analyst"], verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @task
    def reporting_task(self) -> Task:
        return Task(config=self.tasks_config["reporting_task"], output_file="report.md")

    @crew
    def crew(self) -> Crew:
        """Creates the NoobResearchCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
