from typing import Optional, Tuple, List, Dict

from db import database
from .badge_service import BadgeService


class PointService:
    def __init__(self) -> None:
        self.badge_service = BadgeService()

    async def add_points(self, user_id: int, amount: int, reason: str | None = None) -> None:
        user = await database.get_user(user_id)
        if not user:
            return
        points = user.get("points", 0) + amount
        budget = user.get("current_budget", 0.0) + amount
        await database.update_user_data(user_id, points=points, current_budget=budget)
        await self.check_and_update_level(user_id)

    async def deduct_points(self, user_id: int, amount: int, reason: str | None = None) -> bool:
        user = await database.get_user(user_id)
        if not user:
            return False
        if user.get("current_budget", 0.0) < amount:
            return False
        points = max(0, user.get("points", 0) - amount)
        budget = user.get("current_budget", 0.0) - amount
        await database.update_user_data(user_id, points=points, current_budget=budget)
        return True

    async def check_and_update_level(self, user_id: int) -> Optional[Tuple[int, str]]:
        user = await database.get_user(user_id)
        if not user:
            return None
        current_points = user.get("points", 0)
        level_info = await self.calculate_level(current_points)
        if not level_info:
            return None
        new_level = level_info[0]
        if new_level != user.get("level"):
            await database.update_user_data(user_id, level=new_level)
            await self.badge_service.check_level_badge(user_id, new_level)
            return level_info
        return None

    async def calculate_level(self, points: int) -> Optional[Tuple[int, str]]:
        level = await database.get_level_for_points(points)
        if level:
            return level["level_id"], level["level_name"]
        return None

    async def get_user_ranking_position(self, user_id: int) -> Optional[int]:
        return await database.get_user_rank_position(user_id)

    async def get_top_users(self, limit: int = 10) -> List[Dict]:
        return await database.get_top_users(limit)
