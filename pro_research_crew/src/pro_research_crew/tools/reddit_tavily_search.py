import os
from typing import Type

from crewai_tools import BaseTool
from pydantic import BaseModel, PrivateAttr
from tavily import TavilyClient

from pro_research_crew.tools.tavily_search_tool import TavilySearchToolInput


class RedditTavilySearchTool(BaseTool):
    name: str = "Reddit Search Tool"
    description: str = "Search Reddit using Tavily"
    args_schema: Type[BaseModel] = TavilySearchToolInput

    _tavily_client: TavilyClient = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def _run(self, query: str, max_results: int) -> str:
        return self._tavily_client.search(f"Reddit: {query}", max_results=max_results)
