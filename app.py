from flask import Flask, render_template, request, jsonify, session
import uuid
import logging
from weather_providers import OpenMeteoWeatherProvider
from geocoding import OpenWeatherMapGeocoding
from city_suggesters import OpenWeatherMapCitySuggester
from database import SQLiteDatabase

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Конфигурация
OPENWEATHERMAP_API_KEY = "9833bc0a05846bb0c70b50e02690de17"
DB_PATH = 'users.db'

# Инициализация зависимостей
logger.debug("Initializing dependencies...")
geocoding_provider = OpenWeatherMapGeocoding(OPENWEATHERMAP_API_KEY)
weather_provider = OpenMeteoWeatherProvider(geocoding_provider)
city_suggester = OpenWeatherMapCitySuggester(OPENWEATHERMAP_API_KEY)
database = SQLiteDatabase(DB_PATH)
logger.debug("Dependencies initialized")


@app.before_request
def load_user():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    logger.debug(f"User session: {session.get('user_id')}")


@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '')
    logger.debug(f"Autocomplete query: {query}")
    suggestions = city_suggester.get_suggestions(query)
    logger.debug(f"Suggestions: {suggestions}")
    return jsonify(suggestions)


@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    user_id = session.get('user_id')
    logger.debug(f"Request method: {request.method}")

    if request.method == 'POST':
        city = request.form.get('city')
        logger.debug(f"City from form: {city}")

        if city:
            logger.debug("Getting weather data...")
            weather = weather_provider.get_weather(city)
            logger.debug(f"Weather data: {weather}")

            if weather:
                logger.debug("Updating database...")
                database.add_search_history(user_id, city)
                database.update_city_stats(city)
            else:
                logger.debug("Failed to get weather data")

    history = database.get_search_history(user_id)
    top_cities = database.get_top_cities()
    logger.debug(f"History: {history}, Top cities: {top_cities}")

    return render_template(
        'index.html',
        weather=weather,
        history=history,
        top_cities=top_cities
    )


@app.route('/stats')
def stats():
    top_cities = database.get_top_cities(limit=10)
    logger.debug(f"Stats: {top_cities}")
    return render_template('stats.html', top_cities=top_cities)


if __name__ == '__main__':
    app.run(debug=True)