from datetime import datetime
from typing import List, Set

import requests
import os
from dotenv import load_dotenv

from src.ingestion.data_reception.base_datasource import DataSource, NormalizedData

load_dotenv()
CRYPTOCOMPARE_API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")


class CryptoCompareDataSource(DataSource):
    def fetch_data(self, query=None, exclude_categories=None) -> Set[NormalizedData]:
        base_url = "https://min-api.cryptocompare.com/data/v2/news/"
        params = {
            "categories": ",".join(query) if query else None,
            "excludeCategories": ",".join(exclude_categories) if exclude_categories else None,
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()["Data"]
        return self.normalize_data(data)

    def normalize_data(self, data: list) -> Set[NormalizedData]:
        """
        Нормалізація даних криптовалют у формат NormalizedData.
        """
        normalized_crypto = {
            NormalizedData(
                title=article["title"],
                author=None,  # CryptoCompare не надає інформацію про автора
                description=None,  # Логіка для створення короткого опису може бути додана тут
                content=article.get("body"),
                url=article["url"],
                image_url=article.get("imageurl"),
                published_at=datetime.utcfromtimestamp(article["published_on"]).isoformat(),
                source=article["source_info"]["name"],
            )
            for article in data
        }
        return normalized_crypto


def fetch_cryptocompare_news(categories=None, exclude_categories=None):

    url = "https://min-api.cryptocompare.com/data/v2/news/"

    # Параметри запиту
    params = {
        "lang": "EN",  # Мова новин
    }

    if categories:
        params["categories"] = categories
    if exclude_categories:
        params["excludeCategories"] = exclude_categories

    headers = {
        "authorization": f"Apikey {CRYPTOCOMPARE_API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            news = data.get("Data", [])
            # Вибираємо заголовок, джерело та URL для кожної новини
            return [
                {"title": item["title"], "source": item["source"], "url": item["url"]}
                for item in news
            ]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []