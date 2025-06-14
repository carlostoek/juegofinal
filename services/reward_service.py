from datetime import datetime
from typing import List, Dict

import aiosqlite
from aiogram import Bot

from db.database import DB_PATH, get_user
from .point_service import PointService
from .badge_service import BadgeService


class RewardService:
    def __init__(self) -> None:
        self.point_service = PointService()
        self.badge_service = BadgeService()

    async def get_all_rewards(self) -> List[Dict]:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT * FROM rewards")
            rows = await cursor.fetchall()
            cols = [c[0] for c in cursor.description]
            return [dict(zip(cols, r)) for r in rows]

    async def can_afford(self, user_id: int, reward_id: int) -> bool:
        user = await get_user(user_id)
        if not user:
            return False
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT cost_points FROM rewards WHERE reward_id=?", (reward_id,))
            row = await cursor.fetchone()
            if not row:
                return False
            cost = row[0]
        return user.get("current_budget", 0) >= cost

    async def redeem_reward(self, user_id: int, reward_id: int) -> bool:
        if not await self.can_afford(user_id, reward_id):
            return False
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT cost_points FROM rewards WHERE reward_id=?", (reward_id,))
            row = await cursor.fetchone()
            if not row:
                return False
            cost = row[0]
        success = await self.point_service.deduct_points(user_id, cost)
        if not success:
            return False
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO user_rewards(user_id, reward_id, purchase_date) VALUES (?,?,?)",
                (user_id, reward_id, datetime.utcnow().isoformat()),
            )
            await db.commit()
        await self.award_first_redeem_badge(user_id)
        return True

    async def deliver_reward(self, user_id: int, reward_id: int, bot: Bot) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                "SELECT reward_type, content_data FROM rewards WHERE reward_id=?",
                (reward_id,),
            )
            row = await cursor.fetchone()
            if not row:
                return
            r_type, content = row
        if r_type == "text":
            await bot.send_message(user_id, content)
        elif r_type == "file":
            await bot.send_document(user_id, content)
        else:
            await bot.send_message(user_id, "Recompensa entregada")

    async def award_first_redeem_badge(self, user_id: int) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                "SELECT COUNT(*) FROM user_rewards WHERE user_id=?",
                (user_id,),
            )
            row = await cursor.fetchone()
            if row and row[0] == 1:
                cur = await db.execute(
                    "SELECT badge_id FROM badges WHERE name=?",
                    ("Primer Canje",),
                )
                b_row = await cur.fetchone()
                if b_row:
                    await self.badge_service.award_badge(user_id, b_row[0])
