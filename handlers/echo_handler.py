from aiogram import Router, types

router = Router()


@router.message()
async def echo(message: types.Message):
    if message.text:
        await message.answer(message.text)
