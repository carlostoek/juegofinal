import asyncio
from datetime import datetime

import aiosqlite

from db.database import DB_PATH
from services.point_service import PointService
from services.badge_service import BadgeService
from services.mission_service import MissionService
from services.auction_service import AuctionService
import random


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
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(
            "UPDATE daily_interaction_limits SET interaction_count=0, last_reset_date=?",
            (today,),
        )
        await db.commit()


async def award_permanence_points_job(bot) -> None:
    point_service = PointService()
    badge_service = BadgeService()
    async with aiosqlite.connect(str(DB_PATH)) as db:
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


async def check_and_award_missions(bot) -> None:
    mission_service = MissionService()
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cursor = await db.execute(
            "SELECT mission_id FROM missions WHERE (active_from IS NULL OR active_from<=?) AND (active_until IS NULL OR active_until>=?)",
            (now, now),
        )
        missions = await cursor.fetchall()
        user_cur = await db.execute("SELECT user_id FROM users")
        users = await user_cur.fetchall()
    for (mission_id,) in missions:
        for (user_id,) in users:
            if await mission_service.check_user_mission_completion(user_id, mission_id, {}):
                await mission_service.complete_mission(user_id, mission_id)


async def finalize_auctions_job(bot) -> None:
    auction_service = AuctionService()
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cursor = await db.execute(
            "SELECT auction_id FROM auctions WHERE status='active' AND end_time<=?",
            (now,),
        )
        auctions = await cursor.fetchall()
    for (auction_id,) in auctions:
        await auction_service.finalize_auction(auction_id, bot)


async def run_monthly_raffle(bot) -> None:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cur = await db.execute("SELECT user_id, points FROM users")
        data = await cur.fetchall()
    if not data:
        return
    users, weights = zip(*data)
    winner = random.choices(users, weights=weights, k=1)[0]
    await bot.send_message(winner, "\ud83c\udf89 Ganaste el sorteo mensual!")


async def run_weekly_mini_raffle(bot) -> None:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cursor = await db.execute(
            "SELECT user_id FROM weekly_ranking_activity ORDER BY total_activity_points DESC LIMIT 10"
        )
        rows = await cursor.fetchall()
    if rows:
        winner = random.choice([r[0] for r in rows])
        await bot.send_message(winner, "\ud83c\udf81 Ganaste el mini sorteo semanal!")


async def update_weekly_activity_ranking(bot=None) -> None:
    week = datetime.utcnow().isocalendar()[1]
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cur = await db.execute("SELECT user_id, weekly_streak_permanence, total_spent FROM users")
        rows = await cur.fetchall()
        for user_id, activity, spent in rows:
            await db.execute(
                "INSERT INTO weekly_ranking_activity(user_id, week_number, total_activity_points, total_purchase_amount) VALUES (?,?,?,?)",
                (user_id, week, activity or 0, spent or 0.0),
            )
        await db.commit()

