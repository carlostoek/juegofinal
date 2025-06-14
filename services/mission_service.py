from datetime import datetime
from typing import Dict

import aiosqlite

from db.database import DB_PATH
from .point_service import PointService


class MissionService:
    def __init__(self) -> None:
        self.point_service = PointService()

    async def create_mission(
        self,
        type: str,
        description: str,
        points_reward: int,
        completion_criteria: str,
        active_from: str,
        active_until: str,
    ) -> int:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                """
                INSERT INTO missions(type, description, points_reward, completion_criteria, active_from, active_until)
                VALUES (?,?,?,?,?,?)
                """,
                (type, description, points_reward, completion_criteria, active_from, active_until),
            )
            await db.commit()
            return cursor.lastrowid

    async def activate_mission(self, mission_id: int) -> None:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            await db.execute(
                "UPDATE missions SET active_from=? WHERE mission_id=?",
                (datetime.utcnow().isoformat(), mission_id),
            )
            await db.commit()

    async def check_user_mission_completion(self, user_id: int, mission_id: int, current_data: Dict) -> bool:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                "SELECT completion_criteria FROM missions WHERE mission_id=?",
                (mission_id,),
            )
            row = await cursor.fetchone()
            if not row:
                return False
            criteria = row[0]
        try:
            required = int(criteria)
            value = int(current_data.get("value", 0))
            return value >= required
        except Exception:
            return False

    async def complete_mission(self, user_id: int, mission_id: int) -> None:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                "SELECT points_reward FROM missions WHERE mission_id=?",
                (mission_id,),
            )
            row = await cursor.fetchone()
            if not row:
                return
            points = row[0]
        await self.point_service.add_points(user_id, points, reason="mission")
        async with aiosqlite.connect(str(DB_PATH)) as db:
            await db.execute(
                "INSERT INTO user_missions(user_id, mission_id, completed, completion_date) VALUES (?,?,?,?)",
                (user_id, mission_id, True, datetime.utcnow().isoformat()),
            )
            await db.commit()
