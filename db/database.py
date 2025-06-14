import aiosqlite
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

# Use an absolute path for the database file so that it is
# created consistently regardless of the working directory.
DB_PATH = Path(__file__).resolve().parent / "bot.db"

async def init_db() -> None:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                is_admin BOOLEAN DEFAULT 0,
                join_date TEXT,
                points INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                current_budget REAL DEFAULT 0.0,
                last_reaction_date TEXT,
                weekly_streak_permanence INTEGER DEFAULT 0,
                total_spent REAL DEFAULT 0.0,
                purchases_count INTEGER DEFAULT 0,
                referrals_count INTEGER DEFAULT 0
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS levels (
                level_id INTEGER PRIMARY KEY,
                level_name TEXT,
                min_points INTEGER,
                max_points INTEGER,
                benefits_description TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS badges (
                badge_id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                image_url TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS user_badges (
                user_id INTEGER,
                badge_id INTEGER,
                obtained_date TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS reactions_log (
                log_id INTEGER PRIMARY KEY,
                message_id INTEGER,
                user_id INTEGER,
                reaction_type TEXT,
                reaction_date TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_interaction_limits (
                user_id INTEGER PRIMARY KEY,
                interaction_count INTEGER,
                last_reset_date TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS polls (
                poll_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                creator_id INTEGER,
                message_id INTEGER,
                yes_count INTEGER DEFAULT 0,
                no_count INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS poll_votes (
                vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
                poll_id INTEGER,
                user_id INTEGER,
                vote_type TEXT,
                voted_at TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS purchases (
                purchase_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                amount_mxn REAL,
                points_awarded INTEGER,
                purchase_date TEXT,
                is_renewal BOOLEAN,
                is_early_renewal BOOLEAN
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS rewards (
                reward_id INTEGER PRIMARY KEY,
                name TEXT,
                cost_points INTEGER,
                description TEXT,
                reward_type TEXT,
                content_data TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS user_rewards (
                user_id INTEGER,
                reward_id INTEGER,
                purchase_date TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS missions (
                mission_id INTEGER PRIMARY KEY,
                type TEXT,
                description TEXT,
                points_reward INTEGER,
                completion_criteria TEXT,
                active_from TEXT,
                active_until TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS user_missions (
                user_id INTEGER,
                mission_id INTEGER,
                completed BOOLEAN,
                completion_date TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS auctions (
                auction_id INTEGER PRIMARY KEY,
                item_name TEXT,
                description TEXT,
                start_time TEXT,
                end_time TEXT,
                winner_user_id INTEGER,
                winning_bid INTEGER,
                status TEXT DEFAULT 'active'
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS bids (
                bid_id INTEGER PRIMARY KEY,
                auction_id INTEGER,
                user_id INTEGER,
                bid_amount INTEGER,
                bid_time TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_gifts (
                gift_id INTEGER PRIMARY KEY,
                description TEXT,
                points_reward INTEGER,
                gift_type TEXT,
                content TEXT,
                active_date TEXT UNIQUE
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS claimed_daily_gifts (
                user_id INTEGER,
                gift_id INTEGER,
                claimed_date TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS weekly_ranking_activity (
                user_id INTEGER,
                week_number INTEGER,
                total_activity_points INTEGER,
                total_purchase_amount REAL
            )
            """
        )
        await db.commit()

async def create_user(user_id: int, username: str | None, full_name: str) -> None:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cursor = await db.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
        if await cursor.fetchone():
            return
        join_date = datetime.utcnow().isoformat()
        await db.execute(
            """
            INSERT INTO users(user_id, username, full_name, join_date, points)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, username, full_name, join_date, 50),
        )
        await db.commit()

async def get_user(user_id: int) -> Optional[Dict]:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cursor = await db.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = await cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        return None

async def update_user_data(user_id: int, **kwargs) -> None:
    if not kwargs:
        return
    fields = ", ".join(f"{k}=?" for k in kwargs)
    values = list(kwargs.values()) + [user_id]
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(f"UPDATE users SET {fields} WHERE user_id=?", values)
        await db.commit()


async def get_level_for_points(points: int) -> Optional[Dict]:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cursor = await db.execute(
            """
            SELECT * FROM levels
            WHERE min_points<=? AND max_points>=?
            ORDER BY level_id LIMIT 1
            """,
            (points, points),
        )
        row = await cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        return None


async def get_next_level(points: int) -> Optional[Dict]:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cursor = await db.execute(
            "SELECT * FROM levels WHERE min_points>? ORDER BY min_points LIMIT 1",
            (points,),
        )
        row = await cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        return None


async def get_top_users(limit: int = 10) -> list[Dict]:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cursor = await db.execute(
            "SELECT * FROM users ORDER BY points DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, r)) for r in rows]


async def get_user_rank_position(user_id: int) -> Optional[int]:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cursor = await db.execute(
            "SELECT points FROM users WHERE user_id=?",
            (user_id,),
        )
        row = await cursor.fetchone()
        if not row:
            return None
        points = row[0]
        cursor = await db.execute(
            "SELECT COUNT(*) FROM users WHERE points>?",
            (points,),
        )
        higher = await cursor.fetchone()
        if higher:
            return higher[0] + 1
        return 1
