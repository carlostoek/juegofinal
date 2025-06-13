import sqlite3
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """Simple user representation."""

    id: int
    username: str
    full_name: str
    join_date: datetime

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


async def get_user(user_id: int) -> User | None:
    """Retrieve a user from the database."""
    conn = _get_connection()
    try:
        cur = conn.execute(
            "SELECT id, username, full_name, join_date FROM users WHERE id = ?",
            (user_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return User(
            id=row[0],
            username=row[1],
            full_name=row[2],
            join_date=datetime.fromisoformat(row[3]),
        )
    finally:
        conn.close()


async def list_users() -> list[User]:
    """Return all registered users."""
    conn = _get_connection()
    try:
        cur = conn.execute(
            "SELECT id, username, full_name, join_date FROM users ORDER BY join_date"
        )
        rows = cur.fetchall()
        return [
            User(
                id=row[0],
                username=row[1],
                full_name=row[2],
                join_date=datetime.fromisoformat(row[3]),
            )
            for row in rows
        ]
    finally:
        conn.close()


async def remove_user(user_id: int) -> None:
    """Delete a user from the database."""
    conn = _get_connection()
    try:
        with conn:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    finally:
        conn.close()
