from datetime import datetime
import aiosqlite

from db.database import DB_PATH, get_user, update_user_data
from .point_service import PointService


class PurchaseService:
    def __init__(self) -> None:
        self.point_service = PointService()

    async def record_purchase(self, user_id: int, amount_mxn: float, is_renewal: bool = False, is_early_renewal: bool = False) -> int:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            cursor = await db.execute(
                "INSERT INTO purchases(user_id, amount_mxn, points_awarded, purchase_date, is_renewal, is_early_renewal) VALUES (?,?,?,?,?,?)",
                (user_id, amount_mxn, 0, datetime.utcnow().isoformat(), is_renewal, is_early_renewal),
            )
            await db.commit()
            purchase_id = cursor.lastrowid
        user = await get_user(user_id)
        if user:
            total = (user.get("total_spent", 0.0) or 0.0) + amount_mxn
            count = (user.get("purchases_count", 0) or 0) + 1
            await update_user_data(user_id, total_spent=total, purchases_count=count)
        return purchase_id

    async def award_purchase_points(self, user_id: int, amount_mxn: float) -> int:
        points = int(amount_mxn)
        await self.point_service.add_points(user_id, points, reason="purchase")
        async with aiosqlite.connect(str(DB_PATH)) as db:
            await db.execute(
                "UPDATE purchases SET points_awarded=? WHERE user_id=? AND points_awarded=0 ORDER BY purchase_id DESC LIMIT 1",
                (points, user_id),
            )
            await db.commit()
        return points

    async def check_bonus_purchases(self, user_id: int) -> None:
        user = await get_user(user_id)
        if not user:
            return
        if user.get("purchases_count", 0) == 5:
            await self.point_service.add_points(user_id, 50, reason="bonus_5_purchases")
        if user.get("total_spent", 0) >= 10000:
            await self.point_service.add_points(user_id, 100, reason="big_spender_vip")
