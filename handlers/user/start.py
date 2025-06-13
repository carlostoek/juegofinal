from datetime import datetime

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from services.user_service import add_user
from services.point_service import point_service
from config import settings

router = Router()


def build_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return main menu keyboard depending on user role."""
    if user_id in settings.admin_ids:
        buttons = [
            [InlineKeyboardButton(text="Administraci\u00f3n", callback_data="admin")],
            [InlineKeyboardButton(text="Configuraci\u00f3n", callback_data="config")],
            [InlineKeyboardButton(text="Gamificaci\u00f3n", callback_data="gamify")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="Perfil", callback_data="profile")],
            [InlineKeyboardButton(text="Avance", callback_data="progress")],
            [InlineKeyboardButton(text="Budgets", callback_data="budget")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


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

    keyboard = build_menu(user.id)

    await message.answer(
        f"Welcome, {user.full_name}!", reply_markup=keyboard
    )


@router.message(Command("menu"))
async def menu(message: types.Message) -> None:
    """Show the main menu again."""
    keyboard = build_menu(message.from_user.id)
    await message.answer("Men\u00fa:", reply_markup=keyboard)
