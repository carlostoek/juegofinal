from datetime import datetime

import aiosqlite

from db.database import DB_PATH
from .point_service import PointService


class PollService:
    def __init__(self) -> None:
        self.point_service = PointService()

    async def create_poll(self, question: str, creator_id: int, message_id: int | None = None) -> int:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                "INSERT INTO polls(question, creator_id, message_id, created_at) VALUES (?,?,?,?)",
                (question, creator_id, message_id, datetime.utcnow().isoformat()),
            )
            await db.commit()
            return cursor.lastrowid

    async def update_poll_message_id(self, poll_id: int, message_id: int) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE polls SET message_id=? WHERE poll_id=?",
                (message_id, poll_id),
            )
            await db.commit()

    async def record_vote(self, poll_id: int, user_id: int, vote_type: str) -> bool:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                "SELECT is_active FROM polls WHERE poll_id=?",
                (poll_id,),
            )
            poll_row = await cursor.fetchone()
            if not poll_row or not poll_row[0]:
                return False
            cursor = await db.execute(
                "SELECT 1 FROM poll_votes WHERE poll_id=? AND user_id=?",
                (poll_id, user_id),
            )
            if await cursor.fetchone():
                return False
            await db.execute(
                "INSERT INTO poll_votes(poll_id, user_id, vote_type, voted_at) VALUES (?,?,?,?)",
                (poll_id, user_id, vote_type, datetime.utcnow().isoformat()),
            )
            column = "yes_count" if vote_type == "yes" else "no_count"
            await db.execute(
                f"UPDATE polls SET {column}={column}+1 WHERE poll_id=?",
                (poll_id,),
            )
            await db.commit()
            return True

    async def get_poll_results(self, poll_id: int) -> tuple[int, int] | None:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                "SELECT yes_count, no_count FROM polls WHERE poll_id=?",
                (poll_id,),
            )
            row = await cursor.fetchone()
            if row:
                return row[0], row[1]
            return None

    async def deactivate_poll(self, poll_id: int) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE polls SET is_active=0 WHERE poll_id=?",
                (poll_id,),
            )
            await db.commit()

    async def award_poll_points(self, user_id: int) -> None:
        await self.point_service.add_points(user_id, 5, reason="poll_vote")

