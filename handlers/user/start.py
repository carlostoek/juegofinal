from datetime import datetime

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F

from services.user_service import add_user
from services.point_service import point_service

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    user = message.from_user
    # store user info in database
    await add_user(
        user_id=user.id,
        username=user.username or "",
        full_name=user.full_name,
        join_date=message.date or datetime.utcnow(),
    )
    # add registration points
    point_service.register_user(str(user.id))

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Configuración", callback_data="config")],
            [InlineKeyboardButton(text="Administración", callback_data="admin")],
        ]
    )

    await message.answer(
        f"Bienvenido, {user.full_name}!", reply_markup=keyboard
    )


@router.callback_query(F.data == "config")
async def config_menu(callback: types.CallbackQuery) -> None:
    await callback.message.answer("Menú de configuración (pendiente)")
    await callback.answer()


@router.callback_query(F.data == "admin")
async def admin_menu(callback: types.CallbackQuery) -> None:
    await callback.message.answer("Menú de administración (pendiente)")
    await callback.answer()
