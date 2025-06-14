from aiogram import Router
from aiogram.filters import Command
from aiogram import types

from services.user_service import UserService
from utils.keyboards import start_keyboard

router = Router()
user_service = UserService()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user = await user_service.register_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
    )
    is_admin = bool(user.get("is_admin")) if user else False
    text = f"\u2705 Bienvenido {message.from_user.full_name}!"
    await message.answer(text, reply_markup=start_keyboard(is_admin))


@router.message(Command("menu"))
async def cmd_menu(message: types.Message):
    user = await user_service.get_user_profile(message.from_user.id)
    is_admin = bool(user.get("is_admin")) if user else False
    await message.answer("Men\u00fa", reply_markup=start_keyboard(is_admin))
