from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import asyncio
from services.weather_service import get_weather
from utils.geocoding import get_coordinates
from services.history_service import save_search, get_stats
from models.history_model import init_db
from services.location_service import suggest_locations

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    last_city = request.cookies.get('last_city', '')
    return render_template('index.html', last_city=last_city)

@app.route('/weather/<city>')
def show_weather(city):
    try:
        lat, lon = asyncio.run(get_coordinates(city))
    except ValueError:
        return "Город не найден", 404

    weather_data = asyncio.run(get_weather(lat, lon))

    user_id = request.cookies.get('user_id') or "anon_" + city
    save_search(user_id, city)

    response = make_response(render_template('weather.html', data=weather_data, city=city))
    response.set_cookie('user_id', user_id)
    response.set_cookie('last_city', city, max_age=60 * 60 * 24 * 7)
    return response

@app.route('/api/suggest')
def suggest():
    query = request.args.get('query')
    results = asyncio.run(suggest_locations(query))
    return jsonify(results)

@app.route('/api/history/stats')
def stats():
    return jsonify(asyncio.run(get_stats()))

if __name__ == '__main__':
    app.run(debug=True)