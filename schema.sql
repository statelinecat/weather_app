CREATE TABLE IF NOT EXISTS city_stats (
    city TEXT PRIMARY KEY,
    count INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS search_history (
    user_id TEXT,
    city TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_search_history_user_id ON search_history(user_id);