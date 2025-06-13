from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "/help")
async def help_handler(message: Message) -> None:
    await message.answer(
        "Use /profile to view your info, /level to see your level. Earn points daily"
    )
