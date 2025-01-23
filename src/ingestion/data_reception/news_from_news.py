import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Ключ API для NewsAPI (зберігається в .env)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

BASE_URL = "https://newsapi.org/v2/everything"

def fetch_market_news(query="crypto", language="en", sort_by="publishedAt"):
    params = {
        "q": query,
        "language": language,
        "sortBy": sort_by,
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        return articles
    else:
        print(f"Error: {response.status_code}")
        return []

if __name__ == "__main__":
    news = fetch_market_news(query="Trump crypto")
    for i, article in enumerate(news[:5], 1):
        print(f"{i}. {article['title']} - {article['source']['name']}")
        print(f"Link: {article['url']}")
