# geocoding.py
import requests
from abc import ABC, abstractmethod
from typing import Tuple, Optional

class IGeocodingProvider(ABC):
    @abstractmethod
    def get_coordinates(self, city: str) -> Tuple[Optional[float], Optional[float]]:
        pass

class OpenWeatherMapGeocoding(IGeocodingProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_coordinates(self, city: str) -> Tuple[Optional[float], Optional[float]]:
        url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            'q': city,
            'limit': 1,
            'appid': self.api_key
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return float(data[0]['lat']), float(data[0]['lon'])
        except Exception:
            pass
        return None, None