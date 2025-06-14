from datetime import datetime

import aiosqlite

from db.database import DB_PATH, update_user_data
from .point_service import PointService


class ReactionService:
    def __init__(self) -> None:
        self.point_service = PointService()

    async def _increment_interaction(self, user_id: int, db):
        today = datetime.utcnow().date().isoformat()
        cursor = await db.execute(
            "SELECT interaction_count, last_reset_date FROM daily_interaction_limits WHERE user_id=?",
            (user_id,),
        )
        row = await cursor.fetchone()
        if row:
            count, last_reset = row
            if last_reset != today:
                count = 0
                await db.execute(
                    "UPDATE daily_interaction_limits SET interaction_count=0, last_reset_date=? WHERE user_id=?",
                    (today, user_id),
                )
            await db.execute(
                "UPDATE daily_interaction_limits SET interaction_count=? WHERE user_id=?",
                (count + 1, user_id),
            )
        else:
            await db.execute(
                "INSERT INTO daily_interaction_limits(user_id, interaction_count, last_reset_date) VALUES (?,?,?)",
                (user_id, 1, today),
            )

    async def can_react_today(self, user_id: int) -> bool:
        today = datetime.utcnow().date().isoformat()
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                "SELECT interaction_count, last_reset_date FROM daily_interaction_limits WHERE user_id=?",
                (user_id,),
            )
            row = await cursor.fetchone()
            if not row:
                return True
            count, last_reset = row
            if last_reset != today:
                return True
            return count < 4  # 4 interactions * 5 points = 20

    async def record_reaction(self, message_id: int, user_id: int, reaction_type: str) -> None:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            await db.execute(
                "INSERT INTO reactions_log(message_id, user_id, reaction_type, reaction_date) VALUES (?,?,?,?)",
                (message_id, user_id, reaction_type, datetime.utcnow().isoformat()),
            )
            await self._increment_interaction(user_id, db)
            await db.commit()

    async def award_reaction_points(self, user_id: int) -> None:
        await self.point_service.add_points(user_id, 5, reason="reaction")
        await update_user_data(user_id, last_reaction_date=datetime.utcnow().isoformat())

