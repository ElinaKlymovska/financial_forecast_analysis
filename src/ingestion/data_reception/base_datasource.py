from abc import ABC, abstractmethod


class DataSource(ABC):
    """
    Абстрактний базовий клас для джерел даних.
    """

    @abstractmethod
    def fetch_data(self, query=None, exclude_categories=None):
        pass
