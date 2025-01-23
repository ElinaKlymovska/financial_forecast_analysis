import requests
import os
from dotenv import load_dotenv

load_dotenv()
CRYPTOCOMPARE_API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")


def fetch_cryptocompare_news(categories=None, exclude_categories=None):

    url = "https://min-api.cryptocompare.com/data/v2/news/"

    # Параметри запиту
    params = {
        "lang": "EN",  # Мова новин
    }

    if categories:# Наприклад, "Blockchain,Crypto"
        params["categories"] = categories
    if exclude_categories:
        params["excludeCategories"] = exclude_categories  # Наприклад, "Mining"

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


if __name__ == "__main__":

    # Отримати новини без фільтрів
    cryptocompare_news = fetch_cryptocompare_news(categories="Blockchain,Crypto")

    # Вивід новин
    if not cryptocompare_news:
        print("No news found.")
    else:
        for i, article in enumerate(cryptocompare_news, 1):
            print(f"{i}. {article['title']}")
            print(f"Source: {article['source']}")
            print(f"Link: {article['url']}\n")
