from datetime import datetime

from db import database
from .point_service import PointService


class DailyRewardService:
    def __init__(self) -> None:
        self.point_service = PointService()

    async def claim_reward(self, user_id: int) -> bool:
        today = datetime.utcnow().date().isoformat()
        last_claim = await database.get_last_daily_claim(user_id)
        if last_claim == today:
            return False
        await self.point_service.add_points(user_id, 10, reason="daily_reward")
        await database.update_daily_claim(user_id, today)
        return True
