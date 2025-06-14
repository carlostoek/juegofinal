import asyncio

from bot import bot, dp
from handlers import register_handlers


def register_all_handlers() -> None:
    dp.include_router(register_handlers())


async def main() -> None:
    register_all_handlers()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
