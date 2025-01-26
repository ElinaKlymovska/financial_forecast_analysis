import logging
from src.ingestion.data_reception.base_datasource import DataSource
import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


class NewsAPIDataSource(DataSource):
    def fetch_data(self, query=None, exclude_categories=None):
        base_url = "https://newsapi.org/v2/everything"
        logging.info("Fetching news data from the News API")

        params = {"apiKey": NEWS_API_KEY, "language": "en"}

        if query:
            params["q"] = query
        if exclude_categories:
            params["excludeDomains"] = ",".join(exclude_categories) if isinstance(exclude_categories, list) else exclude_categories

        response = requests.get(base_url, params=params)
        response.raise_for_status()

        raw_data = response.json().get("articles", [])
        return raw_data


def fetch_market_news(query = None, exclude = None):
    base_url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "excludeDomains": exclude,
        "apiKey": NEWS_API_KEY,
        "language": "en"
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json().get("articles", [])
