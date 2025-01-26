from src.ingestion.data_reception.news_from_news import NewsAPIDataSource
from src.ingestion.data_reception.сrypto_сompare import CryptoCompareDataSource


def ingest_data(query=None, exclude_categories=None):
    """
    Завантаження даних з усіх джерел з врахуванням фільтрів.
    """
    crypto_source = CryptoCompareDataSource()
    news_source = NewsAPIDataSource()

    crypto_data = crypto_source.fetch_data(query=query, exclude_categories=exclude_categories)
    news_data = news_source.fetch_data(query=query, exclude_categories=exclude_categories)

    combined_data = crypto_data + news_data
    return combined_data



