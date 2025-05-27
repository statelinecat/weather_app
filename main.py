from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather(city)
    return render_template('index.html', weather=weather)

def get_weather(city):
    api_key = "9833bc0a05846bb0c70b50e02690de17"

    # Шаг 1: Получение координат по названию города
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}&lang=ru"
    geo_response = requests.get(geo_url)
    if geo_response.status_code != 200 or not geo_response.json():
        return None

    location = geo_response.json()[0]
    lat = location['lat']
    lon = location['lon']

    # Шаг 2: Получение прогноза по координатам
    weather_url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={api_key}&units=metric&lang=ru"
    )
    weather_response = requests.get(weather_url)
    if weather_response.status_code != 200:
        return None

    data = weather_response.json()

    # Формируем прогноз на 5 дней (сегодня + 4)
    forecast = []
    for day in data['daily'][:5]:
        forecast.append({
            'date': datetime.utcfromtimestamp(day['dt']).strftime('%d.%m.%Y'),
            'temperature_day': round(day['temp']['day']),
            'temperature_night': round(day['temp']['night']),
            'description': day['weather'][0]['description'],
            'icon': day['weather'][0]['icon']
        })

    return {
        'city': city,
        'current': {
            'temperature': round(data['current']['temp']),
            'description': data['current']['weather'][0]['description'],
            'icon': data['current']['weather'][0]['icon']
        },
        'forecast': forecast
    }



if __name__ == '__main__':
    app.run(debug=True)