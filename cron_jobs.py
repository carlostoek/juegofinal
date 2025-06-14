import asyncio
from datetime import datetime

import aiosqlite

from db.database import DB_PATH
from services.point_service import PointService
from services.badge_service import BadgeService


class Scheduler:
    def __init__(self) -> None:
        self.jobs: list[callable] = []

    def add_daily_job(self, coro):
        self.jobs.append(coro)

    async def start(self, bot):
        while True:
            for job in self.jobs:
                try:
                    await job(bot)
                except Exception:
                    pass
            await asyncio.sleep(24 * 60 * 60)


async def daily_reset_interaction_limit(bot) -> None:
    today = datetime.utcnow().date().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE daily_interaction_limits SET interaction_count=0, last_reset_date=?",
            (today,),
        )
        await db.commit()


async def award_permanence_points_job(bot) -> None:
    point_service = PointService()
    badge_service = BadgeService()
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id, weekly_streak_permanence FROM users"
        )
        rows = await cursor.fetchall()
        badge_id = None
        cur = await db.execute(
            "SELECT badge_id FROM badges WHERE name=?",
            ("Veterano \u00cdntimo",),
        )
        row = await cur.fetchone()
        if row:
            badge_id = row[0]
        for user_id, streak in rows:
            await point_service.add_points(user_id, 1, reason="permanence")
            new_streak = (streak or 0) + 1
            await db.execute(
                "UPDATE users SET weekly_streak_permanence=? WHERE user_id=?",
                (new_streak, user_id),
            )
            if badge_id and new_streak % 7 == 0:
                await badge_service.award_badge(user_id, badge_id)
        await db.commit()

