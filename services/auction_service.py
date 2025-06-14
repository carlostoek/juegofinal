from datetime import datetime
from typing import Optional

import aiosqlite
from aiogram import Bot

from db.database import DB_PATH
from .point_service import PointService
from .badge_service import BadgeService


class AuctionService:
    def __init__(self) -> None:
        self.point_service = PointService()
        self.badge_service = BadgeService()

    async def create_auction(self, item_name: str, description: str, start_time: str, end_time: str) -> int:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                """
                INSERT INTO auctions(item_name, description, start_time, end_time)
                VALUES (?,?,?,?)
                """,
                (item_name, description, start_time, end_time),
            )
            await db.commit()
            return cursor.lastrowid

    async def place_bid(self, auction_id: int, user_id: int, bid_amount: int) -> bool:
        now = datetime.utcnow().isoformat()
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                "SELECT end_time, status FROM auctions WHERE auction_id=?",
                (auction_id,),
            )
            row = await cursor.fetchone()
            if not row or row[1] != "active" or row[0] <= now:
                return False
            cur = await db.execute(
                "SELECT MAX(bid_amount) FROM bids WHERE auction_id=?",
                (auction_id,),
            )
            max_row = await cur.fetchone()
            max_bid = max_row[0] if max_row and max_row[0] else 0
            if bid_amount <= max_bid:
                return False
            await db.execute(
                "INSERT INTO bids(auction_id, user_id, bid_amount, bid_time) VALUES (?,?,?,?)",
                (auction_id, user_id, bid_amount, now),
            )
            await db.commit()
            return True

    async def finalize_auction(self, auction_id: int, bot: Bot) -> None:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                "SELECT end_time, status FROM auctions WHERE auction_id=?",
                (auction_id,),
            )
            row = await cursor.fetchone()
            if not row or row[1] != "active" or row[0] > datetime.utcnow().isoformat():
                return
            bcur = await db.execute(
                "SELECT user_id, bid_amount FROM bids WHERE auction_id=? ORDER BY bid_amount DESC LIMIT 1",
                (auction_id,),
            )
            bid_row = await bcur.fetchone()
            if not bid_row:
                await db.execute(
                    "UPDATE auctions SET status='finished' WHERE auction_id=?",
                    (auction_id,),
                )
                await db.commit()
                return
            winner, winning_bid = bid_row
        success = await self.point_service.deduct_points(winner, winning_bid)
        async with aiosqlite.connect(str(DB_PATH)) as db:
            await db.execute(
                "UPDATE auctions SET winner_user_id=?, winning_bid=?, status='finished' WHERE auction_id=?",
                (winner, winning_bid, auction_id),
            )
            await db.commit()
        if success:
            await bot.send_message(winner, f"Felicidades! Ganaste la subasta con {winning_bid} puntos")
            await self.award_collector_badge(winner)

    async def award_collector_badge(self, user_id: int) -> None:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                "SELECT badge_id FROM badges WHERE name=?",
                ("Coleccionista Exclusivo",),
            )
            row = await cursor.fetchone()
            if not row:
                return
            badge_id = row[0]
        await self.badge_service.award_badge(user_id, badge_id)
