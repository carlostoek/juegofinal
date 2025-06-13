from dataclasses import dataclass

from aiogram import Router, F
from aiogram.types import Message

# Placeholder service for getting user level and points
@dataclass
class LevelInfo:
    level: int
    points: int

async def get_level_info(user_id: int) -> LevelInfo:
    # In a real implementation this would fetch data from a database
    return LevelInfo(level=1, points=0)

router = Router()


@router.message(F.text == "/level")
async def level_handler(message: Message) -> None:
    info = await get_level_info(message.from_user.id)
    await message.answer(f"You are level {info.level} with {info.points} points")
