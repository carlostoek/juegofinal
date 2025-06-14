from datetime import datetime
from typing import Dict, Optional

import aiosqlite

from db.database import DB_PATH
from .point_service import PointService


class DailyGiftService:
    def __init__(self) -> None:
        self.point_service = PointService()

    async def get_current_daily_gift(self) -> Optional[Dict]:
        today = datetime.utcnow().date().isoformat()
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                "SELECT * FROM daily_gifts WHERE active_date=?",
                (today,),
            )
            row = await cursor.fetchone()
            if not row:
                return None
            columns = [c[0] for c in cursor.description]
            return dict(zip(columns, row))

    async def has_claimed_today(self, user_id: int) -> bool:
        today = datetime.utcnow().date().isoformat()
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                "SELECT 1 FROM claimed_daily_gifts WHERE user_id=? AND claimed_date=?",
                (user_id, today),
            )
            return bool(await cursor.fetchone())

    async def claim_gift(self, user_id: int, gift_id: int) -> Optional[Dict]:
        if await self.has_claimed_today(user_id):
            return None
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                "SELECT description, points_reward, gift_type, content FROM daily_gifts WHERE gift_id=?",
                (gift_id,),
            )
            gift_row = await cursor.fetchone()
            if not gift_row:
                return None
            description, points_reward, gtype, content = gift_row
            await db.execute(
                "INSERT INTO claimed_daily_gifts(user_id, gift_id, claimed_date) VALUES (?,?,?)",
                (user_id, gift_id, datetime.utcnow().date().isoformat()),
            )
            await db.commit()
        if points_reward:
            await self.point_service.add_points(user_id, points_reward, reason="daily_gift")
        return {
            "description": description,
            "points_reward": points_reward,
            "gift_type": gtype,
            "content": content,
        }
