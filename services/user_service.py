from typing import Optional, Dict

from db import database


class UserService:
    async def register_user(self, user_id: int, username: str | None, full_name: str) -> Dict:
        await database.create_user(user_id, username, full_name)
        user = await database.get_user(user_id)
        return user

    async def get_user_profile(self, user_id: int) -> Optional[Dict]:
        return await database.get_user(user_id)

    async def update_user_points(self, user_id: int, delta: int) -> None:
        user = await database.get_user(user_id)
        if not user:
            return
        points = user.get("points", 0) + delta
        await database.update_user_data(user_id, points=points)

    async def is_admin(self, user_id: int) -> bool:
        user = await database.get_user(user_id)
        return bool(user and user.get("is_admin"))
