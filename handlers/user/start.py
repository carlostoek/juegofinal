from datetime import datetime

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from services.user_service import add_user

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

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Profile", callback_data="profile")],
            [InlineKeyboardButton(text="Help", callback_data="help")],
            [InlineKeyboardButton(text="Level", callback_data="level")],
        ]
    )

    await message.answer(
        f"Welcome, {user.full_name}!", reply_markup=keyboard
    )
