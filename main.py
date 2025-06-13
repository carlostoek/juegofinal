import asyncio

from bot import bot, dp
from aiogram import types
from aiogram.filters import Command
from utils import MSG
from handlers.user.start import router as start_router
from handlers.user.profile import router as profile_router
from handlers.user.level import router as level_router
from handlers.user.badges import router as badges_router
from handlers.user.ranking import router as ranking_router
from handlers.user.reaction import router as reaction_router
from handlers.user.polls import router as poll_router
from handlers.user.menu_options import router as menu_router

dp.include_router(start_router)
dp.include_router(profile_router)
dp.include_router(level_router)
dp.include_router(badges_router)
dp.include_router(ranking_router)
dp.include_router(reaction_router)
dp.include_router(poll_router)
dp.include_router(menu_router)


@dp.message(Command("help"))
async def help_handler(message: types.Message) -> None:
    """Send instructions for using the bot."""
    await message.answer(MSG.HELP)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer(message.text)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
