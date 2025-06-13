from aiogram import Router, F, types

from .profile import profile_text
from services.user_service import get_user
from .start import back_markup
from utils import MSG

router = Router()


@router.callback_query(F.data == "profile")
async def handle_profile(query: types.CallbackQuery) -> None:
    user = await get_user(query.from_user.id)
    if user:
        text = profile_text(user)
        await query.message.edit_text(text, reply_markup=back_markup())
    else:
        await query.message.edit_text(MSG.NOT_REGISTERED, reply_markup=back_markup())
    await query.answer()


@router.callback_query(F.data == "budget")
async def handle_budget(query: types.CallbackQuery) -> None:
    await query.message.edit_text(MSG.BUDGET, reply_markup=back_markup())
    await query.answer()


@router.callback_query(F.data == "admin")
async def handle_admin(query: types.CallbackQuery) -> None:
    await query.message.edit_text(MSG.ADMIN_MENU, reply_markup=back_markup())
    await query.answer()


@router.callback_query(F.data == "config")
async def handle_config(query: types.CallbackQuery) -> None:
    await query.message.edit_text(MSG.CONFIG, reply_markup=back_markup())
    await query.answer()


@router.callback_query(F.data == "gamify")
async def handle_gamify(query: types.CallbackQuery) -> None:
    await query.message.edit_text(MSG.GAMIFY, reply_markup=back_markup())
    await query.answer()
