from models.history_model import add_search, get_city_count

def save_search(user_id: str, city: str):
    add_search(user_id, city)

def get_stats():
    return get_city_count()