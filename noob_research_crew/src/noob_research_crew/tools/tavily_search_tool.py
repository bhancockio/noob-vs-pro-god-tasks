import os
from typing import Type

from crewai_tools import BaseTool
from pydantic import BaseModel
from tavily import TavilyClient


class TavilySearchToolInput(BaseModel):
    # query: str = Field(..., description="The query to search the web for.")
    # max_results: int = Field(3, description="The maximum number of results to return.")
    query: str
    max_results: int


class TavilySearchTool(BaseTool):
    name: str = "Tavily Search Tool"
    description: str = "Search the web using Tavily"
    args_schema: Type[BaseModel] = TavilySearchToolInput

    def __init__(self):
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def _run(self, query: str) -> str:
        return self.tavily_client.search(query, max_results=self.max_results)
