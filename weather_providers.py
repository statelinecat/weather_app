import requests
from datetime import datetime
from typing import Dict, Optional, Any
from interfaces import IWeatherProvider
import logging

logger = logging.getLogger(__name__)

class OpenMeteoWeatherProvider(IWeatherProvider):
    def __init__(self, geocoding_provider: 'IGeocodingProvider'):
        self.geocoding_provider = geocoding_provider

    def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        logger.debug(f"Getting coordinates for city: {city}")
        lat, lon = self.geocoding_provider.get_coordinates(city)
        logger.debug(f"Coordinates: {lat}, {lon}")

        if lat is None or lon is None:
            logger.error("Failed to get coordinates")
            return None

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,weathercode",
            "hourly": "temperature_2m,weathercode",
            "timezone": "auto",
            "forecast_days": 7
        }

        try:
            logger.debug(f"Requesting weather data from {url}")
            response = requests.get(url, params=params)
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response text: {response.text[:200]}...")  # Первые 200 символов

            if response.status_code == 200:
                return self._parse_weather_data(response.json(), city)
            else:
                logger.error(f"API returned status {response.status_code}")
        except Exception as e:
            logger.error(f"Error getting weather: {str(e)}")

        return None

    def _parse_weather_data(self, data: Dict, city: str) -> Dict[str, Any]:
        forecast = []
        for i in range(len(data['daily']['time'])):
            code = data['daily']['weathercode'][i]
            forecast.append({
                'date': data['daily']['time'][i],
                'temperature_day': round(data['daily']['temperature_2m_max'][i]),
                'temperature_night': round(data['daily']['temperature_2m_min'][i]),
                'description': self._weather_code_to_text(code),
                'icon': self._get_weather_icon(code)
            })

        now = datetime.now()
        hourly = []
        for i, time_str in enumerate(data['hourly']['time']):
            time_obj = datetime.fromisoformat(time_str)
            if 0 <= (time_obj - now).total_seconds() <= 6 * 3600:
                code = data['hourly']['weathercode'][i]
                hourly.append({
                    'time': time_obj.strftime('%H:%M'),
                    'temp': round(data['hourly']['temperature_2m'][i]),
                    'description': self._weather_code_to_text(code),
                    'icon': self._get_weather_icon(code)
                })

        return {
            'city': city.title(),
            'forecast': forecast,
            'hourly': hourly
        }

    def _get_weather_icon(self, code: int) -> str:
        icon_map = {
            0: "☀️", 1: "🌤", 2: "⛅️", 3: "☁️", 45: "🌫", 48: "🌫",
            51: "🌦", 53: "🌧", 55: "🌧", 61: "🌦", 63: "🌧", 65: "🌧",
            71: "🌨", 73: "❄️", 75: "❄️", 95: "🌩", 99: "⛈"
        }
        return icon_map.get(code, "🌈")

    def _weather_code_to_text(self, code: int) -> str:
        code_map = {
            0: "Ясно", 1: "Преимущественно ясно", 2: "Переменная облачность", 3: "Пасмурно",
            45: "Туман", 48: "Иней", 51: "Морось слабая", 53: "Морось", 55: "Морось сильная",
            61: "Небольшой дождь", 63: "Умеренный дождь", 65: "Сильный дождь",
            71: "Снег слабый", 73: "Умеренный снег", 75: "Сильный снег",
            95: "Гроза", 99: "Гроза с градом"
        }
        return code_map.get(code, "")