from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "9833bc0a05846bb0c70b50e02690de17"  # твой ключ

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather(city)
    return render_template('index.html', weather=weather)

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify([])

    results = response.json()
    cities = []
    for item in results:
        name = item['name']
        country = item.get('country', '')
        state = item.get('state', '')
        display_name = f"{name}, {state + ', ' if state else ''}{country}"
        cities.append(display_name)
    return jsonify(cities)

def get_weather(city):
    # Получаем координаты
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_response = requests.get(geo_url)
    if geo_response.status_code != 200 or not geo_response.json():
        return None

    location = geo_response.json()[0]
    lat = location['lat']
    lon = location['lon']

    # Получаем погоду (OneCall API)
    weather_url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={lat}&lon={lon}&exclude=minutely,alerts&appid={API_KEY}&units=metric&lang=ru"
    )
    weather_response = requests.get(weather_url)
    if weather_response.status_code != 200:
        return None

    data = weather_response.json()

    # Почасовой прогноз (6 ближайших часов)
    hourly = []
    for hour in data['hourly'][:6]:
        hourly.append({
            'time': datetime.utcfromtimestamp(hour['dt']).strftime('%H:%M'),
            'temp': round(hour['temp']),
            'description': hour['weather'][0]['description'],
            'icon': hour['weather'][0]['icon']
        })

    # Прогноз на 5 дней
    forecast = []
    for day in data['daily'][:5]:
        forecast.append({
            'date': datetime.utcfromtimestamp(day['dt']).strftime('%Y-%m-%d'),
            'temperature_day': round(day['temp']['day']),
            'temperature_night': round(day['temp']['night']),
            'description': day['weather'][0]['description'],
            'icon': day['weather'][0]['icon']
        })

    return {
        'city': city.title(),
        'current': {
            'temperature': round(data['current']['temp']),
            'description': data['current']['weather'][0]['description'],
            'icon': data['current']['weather'][0]['icon']
        },
        'hourly': hourly,
        'forecast': forecast
    }

if __name__ == '__main__':
    app.run(debug=True)
