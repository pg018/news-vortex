import os
from httpx import AsyncClient


class GetNewsApi:
    def __init__(self, query: str) -> None:
        self.entered_query = query
        self.get_everything_url = os.environ["NEWSAPI_URL"]
        self.api_key = os.environ["NEWSAPI_API_KEY"]

    async def get_all_news(self):
        """Returns the json object of news retrieved from api call"""
        async with AsyncClient() as client:
            params = {"q": self.entered_query, "apiKey": self.api_key}
            response = await client.get(url=self.get_everything_url, params=params)
            response.raise_for_status()  # raises exceptions
            # print(response.json())
            return response.json()
