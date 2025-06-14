from datetime import datetime
from typing import List, Dict

import aiosqlite
from db.database import DB_PATH


class BadgeService:
    async def award_badge(self, user_id: int, badge_id: int) -> None:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            await db.execute(
                "INSERT INTO user_badges(user_id, badge_id, obtained_date) VALUES (?, ?, ?)",
                (user_id, badge_id, datetime.utcnow().isoformat()),
            )
            await db.commit()

    async def get_user_badges(self, user_id: int) -> List[Dict]:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                """
                SELECT b.badge_id, b.name, b.description, b.image_url, ub.obtained_date
                FROM user_badges ub
                JOIN badges b ON ub.badge_id = b.badge_id
                WHERE ub.user_id=?
                """,
                (user_id,),
            )
            rows = await cursor.fetchall()
            columns = [c[0] for c in cursor.description]
            return [dict(zip(columns, r)) for r in rows]

    async def check_level_badge(self, user_id: int, level_id: int) -> None:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                "SELECT 1 FROM user_badges WHERE user_id=? AND badge_id=?",
                (user_id, level_id),
            )
            if await cursor.fetchone():
                return
            cursor = await db.execute(
                "SELECT badge_id FROM badges WHERE badge_id=?",
                (level_id,),
            )
            if await cursor.fetchone():
                await self.award_badge(user_id, level_id)
