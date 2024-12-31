import os
from typing import Dict, List, Type

import requests
from crewai_tools import BaseTool
from pydantic import BaseModel, Field


class VideoSearchResult(BaseModel):
    video_id: str
    title: str
    channel_id: str
    channel_title: str
    days_since_published: int


class VideoDetails(BaseModel):
    title: str
    view_count: int
    url: str


class YoutubeVideoSearchAndDetailsToolInput(BaseModel):
    keyword: str = Field(..., description="The search keyword.")
    max_results: int = Field(3, description="The maximum number of results to return.")


class YoutubeVideoSearchAndDetailsTool(BaseTool):
    name: str = "Search and Get YouTube Video Details"
    description: str = (
        "Searches YouTube videos based on a keyword and retrieves details for each video."
    )
    args_schema: Type[BaseModel] = YoutubeVideoSearchAndDetailsToolInput
    api_key: str = Field(default_factory=lambda: os.getenv("YOUTUBE_API_KEY"))

    def fetch_video_details_sync(self, video_id: str) -> VideoDetails:
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {"part": "snippet,statistics", "id": video_id, "key": self.api_key}
        response = requests.get(url, params=params)
        response.raise_for_status()
        item = response.json().get("items", [])[0]
        title = item["snippet"]["title"]
        view_count = int(item["statistics"]["viewCount"])
        video_url = f"https://youtube.com/watch?v={video_id}"
        return VideoDetails(title=title, view_count=view_count, url=video_url)

    def _run(self, keyword: str, max_results: int = 3) -> List[Dict]:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": keyword,
            "maxResults": max_results,
            "type": "video",
            "key": self.api_key,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])

        video_details = [
            self.fetch_video_details_sync(item["id"]["videoId"]) for item in items
        ]
        return [video.model_dump() for video in video_details]
