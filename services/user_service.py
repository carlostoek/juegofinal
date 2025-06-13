import sqlite3
from datetime import datetime

DB_PATH = 'bot.db'


def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            join_date TEXT
        )"""
    )
    return conn


async def add_user(user_id: int, username: str, full_name: str, join_date: datetime) -> None:
    conn = _get_connection()
    try:
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO users (id, username, full_name, join_date) VALUES (?, ?, ?, ?)",
                (user_id, username, full_name, join_date.isoformat()),
            )
    finally:
        conn.close()
