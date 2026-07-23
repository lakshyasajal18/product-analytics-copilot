import sqlite3
from pathlib import Path

database_path = Path("data/product_analytics.db")
database_path.parent.mkdir(parents=True, exist_ok=True)

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    device TEXT NOT NULL,
    signup_date TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

connection.commit()
connection.close()

print("Database tables created successfully!")