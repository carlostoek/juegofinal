from aiogram import Router, F
from aiogram.types import Message

from utils import MSG

from services.badge_service import get_badges

router = Router()


@router.message(F.text == "/badges")
async def badges_handler(message: Message) -> None:
    badges = await get_badges(message.from_user.id)
    if not badges:
        await message.answer(MSG.BADGES_NONE)
        return

    lines = [f"{b.name} - {b.description} ({b.date_awarded.date()})" for b in badges]
    await message.answer(MSG.BADGES_LIST_HEADER + "\n".join(lines))
