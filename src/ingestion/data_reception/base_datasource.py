from abc import ABC, abstractmethod
from typing import Set
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class NormalizedData:
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    published_at: Optional[str] = None
    source: Optional[str] = None

    @property
    def short_title(self) -> str:
        """
        Повертає скорочений заголовок.
        """
        return self.title[:30] + "..." if self.title and len(self.title) > 30 else self.title or "No title"

    @short_title.setter
    def short_title(self, value: str):
        """
        Обрізає заголовок до 30 символів перед встановленням.
        """
        self.title = value[:30]


class DataSource(ABC):
    """
    Абстрактний базовий клас для джерел даних.
    """

    @abstractmethod
    def fetch_data(self, query=None, exclude_categories=None) -> Set[NormalizedData]:
        pass

    @abstractmethod
    def normalize_data(self, data: list) -> Set[NormalizedData]:
        pass