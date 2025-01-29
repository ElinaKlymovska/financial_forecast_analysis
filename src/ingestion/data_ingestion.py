from src.ingestion.data_reception.news_from_news import NewsAPIDataSource
from src.ingestion.data_reception.сrypto_сompare import CryptoCompareDataSource, NormalizedData

from typing import Set


def ingest_data(query=None, exclude_categories=None) -> Set[NormalizedData]:
    """
    Load data from all sources with applied filters.
    """
    crypto_source = CryptoCompareDataSource()
    news_source = NewsAPIDataSource()

    crypto_data = crypto_source.fetch_data(query=query, exclude_categories=exclude_categories)
    news_data = news_source.fetch_data(query=query, exclude_categories=exclude_categories)

    combined_data: Set[NormalizedData] = crypto_data.union(news_data)
    return combined_data