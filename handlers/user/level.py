from aiogram import Router, F
from aiogram.types import Message

from utils import MSG

from services.point_service import point_service
from services.badge_service import check_level_badges

router = Router()


@router.message(F.text == "/level")
async def level_handler(message: Message) -> None:
    user_id = message.from_user.id
    level = point_service.get_level(str(user_id))
    points = point_service.get_points(str(user_id))
    await check_level_badges(user_id, level)
    await message.answer(MSG.LEVEL.format(level=level, points=points))
