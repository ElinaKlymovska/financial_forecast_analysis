from src.ingestion.data_reception.data_from_сrypto_сompare import fetch_cryptocompare_news
from src.ingestion.data_reception.news_from_news import fetch_market_news


def ingest_data(query=None):
    # Отримання даних через API
    news_api_data = fetch_market_news(query=query)
    scraped_data = fetch_cryptocompare_news(categories=query)

    articles = news_api_data + scraped_data

    return articles
