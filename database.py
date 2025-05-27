import sqlite3
from typing import List, Tuple, Optional
from interfaces import IDatabase
import logging

logger = logging.getLogger(__name__)

class SQLiteDatabase(IDatabase):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        logger.debug(f"Initializing database at {self.db_path}")
        try:
            conn = sqlite3.connect(self.db_path)
            with open('schema.sql', 'r') as f:
                schema = f.read()
                logger.debug(f"Executing schema: {schema[:100]}...")  # Первые 100 символов
                conn.cursor().executescript(schema)
            conn.commit()
            conn.close()
            logger.debug("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")

    def update_city_stats(self, city: str) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO city_stats (city, count) VALUES (?, 1)
            ON CONFLICT(city) DO UPDATE SET count = count + 1
        """, (city,))
        conn.commit()
        conn.close()

    def add_search_history(self, user_id: str, city: str) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO search_history (user_id, city) VALUES (?, ?)", (user_id, city))
        conn.execute("""
            DELETE FROM search_history 
            WHERE rowid NOT IN (
                SELECT rowid FROM search_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5
            )""", (user_id,))
        conn.commit()
        conn.close()

    def get_search_history(self, user_id: str) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT city FROM search_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5", (user_id,))
        result = [row[0] for row in cur.fetchall()]
        conn.close()
        return result

    def get_top_cities(self, limit: int = 5) -> List[Tuple[str, int]]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT city, count FROM city_stats ORDER BY count DESC LIMIT ?", (limit,))
        result = cur.fetchall()
        conn.close()
        return result