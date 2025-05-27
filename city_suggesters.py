import requests
from typing import List
from interfaces import ICitySuggester

class OpenWeatherMapCitySuggester(ICitySuggester):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_suggestions(self, query: str) -> List[str]:
        if not query:
            return []

        url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            'q': query,
            'limit': 5,
            'appid': self.api_key
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                suggestions = []
                for item in data:
                    ru_name = item.get('local_names', {}).get('ru')
                    city_name = ru_name if ru_name else item['name']
                    suggestions.append(city_name)
                return list(set(suggestions))[:5]
        except Exception:
            return []