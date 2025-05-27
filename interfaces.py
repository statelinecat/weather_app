from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any


class IWeatherProvider(ABC):
    @abstractmethod
    def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        pass


class ICitySuggester(ABC):
    @abstractmethod
    def get_suggestions(self, query: str) -> List[str]:
        pass


class IDatabase(ABC):
    @abstractmethod
    def update_city_stats(self, city: str) -> None:
        pass

    @abstractmethod
    def add_search_history(self, user_id: str, city: str) -> None:
        pass

    @abstractmethod
    def get_search_history(self, user_id: str) -> List[str]:
        pass

    @abstractmethod
    def get_top_cities(self, limit: int = 5) -> List[Tuple[str, int]]:
        pass