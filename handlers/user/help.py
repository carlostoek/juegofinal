from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "Available commands:\n"
        "/profile - View your info\n"
        "/level - Show your level and points\n"
        "/badges - List your badges\n"
        "/ranking - View the leaderboard"
        " (alias: /leaderboard)"
    )
