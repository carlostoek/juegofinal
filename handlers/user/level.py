from aiogram import Router, F
from aiogram.types import Message

from services.point_service import point_service

router = Router()


@router.message(F.text == "/level")
async def level_handler(message: Message) -> None:
    level = point_service.get_level(str(message.from_user.id))
    points = point_service.get_points(str(message.from_user.id))
    await message.answer(f"You are level {level} with {points} points")
