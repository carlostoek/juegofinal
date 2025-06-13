import asyncio

from bot import bot, dp
from aiogram import types
from aiogram.filters import Command


@dp.message(Command("help"))
async def help_handler(message: types.Message) -> None:
    """Send instructions for using the bot."""
    instructions = (
        "Available commands:\n"
        "/start - Register and open menu\n"
        "/profile - Show your profile\n"
        "/level - Get your level and points\n"
        "/help - Show this message"
    )
    await message.answer(instructions)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer(message.text)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
