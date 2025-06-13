import sqlite3
from typing import Any

DB_PATH = 'bot.db'


def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )"""
    )
    return conn


async def set_config(key: str, value: str) -> None:
    conn = _get_connection()
    try:
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
                (key, value),
            )
    finally:
        conn.close()


async def get_config(key: str, default: Any | None = None) -> Any:
    conn = _get_connection()
    try:
        cur = conn.execute("SELECT value FROM config WHERE key = ?", (key,))
        row = cur.fetchone()
        if row:
            return row[0]
        return default
    finally:
        conn.close()
