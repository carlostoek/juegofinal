from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils import MSG

router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(MSG.HELP)
