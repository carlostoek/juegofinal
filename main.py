import asyncio

from bot import bot, dp
from aiogram import types


@dp.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer(message.text)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
