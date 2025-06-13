import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import List

DB_PATH = 'bot.db'


def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS badges (
            badge_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            description TEXT,
            date_awarded TEXT
        )"""
    )
    return conn


@dataclass
class Badge:
    badge_id: int
    user_id: int
    name: str
    description: str
    date_awarded: datetime


async def award_badge(user_id: int, name: str, description: str) -> None:
    conn = _get_connection()
    try:
        with conn:
            conn.execute(
                "INSERT INTO badges (user_id, name, description, date_awarded) VALUES (?, ?, ?, ?)",
                (user_id, name, description, datetime.utcnow().isoformat()),
            )
    finally:
        conn.close()


async def get_badges(user_id: int) -> List[Badge]:
    conn = _get_connection()
    try:
        cur = conn.execute(
            "SELECT badge_id, user_id, name, description, date_awarded FROM badges WHERE user_id = ? ORDER BY date_awarded",
            (user_id,),
        )
        rows = cur.fetchall()
        return [
            Badge(
                badge_id=row[0],
                user_id=row[1],
                name=row[2],
                description=row[3],
                date_awarded=datetime.fromisoformat(row[4]),
            )
            for row in rows
        ]
    finally:
        conn.close()


async def has_badge(user_id: int, name: str) -> bool:
    conn = _get_connection()
    try:
        cur = conn.execute(
            "SELECT 1 FROM badges WHERE user_id = ? AND name = ?",
            (user_id, name),
        )
        return cur.fetchone() is not None
    finally:
        conn.close()


async def check_level_badges(user_id: int, level: int) -> None:
    milestones = [5, 10, 20]
    for m in milestones:
        if level >= m and not await has_badge(user_id, f"Level {m}"):
            await award_badge(user_id, f"Level {m}", f"Reached level {m}")
