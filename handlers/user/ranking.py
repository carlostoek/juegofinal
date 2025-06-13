from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils import MSG

from services.point_service import point_service
from services.user_service import get_user

router = Router()


@router.message(Command("ranking"))
@router.message(Command("leaderboard"))
async def ranking_handler(message: Message) -> None:
    user_id = str(message.from_user.id)
    leaderboard = point_service.get_leaderboard(10)
    lines = []
    for position, (uid, points) in enumerate(leaderboard, start=1):
        user = await get_user(int(uid))
        name = user.full_name if user else uid
        lines.append(f"{position}. {name} - {points}")

    user_position = point_service.get_position(user_id)
    user_points = point_service.get_points(user_id)

    response = MSG.RANKING_HEADER + "\n".join(lines)
    response += MSG.RANKING_POSITION.format(position=user_position, points=user_points)
    await message.answer(response)
