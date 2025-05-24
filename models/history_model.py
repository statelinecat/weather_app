import sqlite3
import os
from config import DATABASE

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        conn.execute('''
            CREATE TABLE searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                city TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

def add_search(user_id, city):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("INSERT INTO searches (user_id, city) VALUES (?, ?)", (user_id, city))
        conn.commit()

def get_city_count():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT city, COUNT(*) FROM searches GROUP BY city")
        return dict(cur.fetchall())