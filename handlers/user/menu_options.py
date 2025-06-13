from aiogram import Router, F, types

from .profile import profile_handler

router = Router()


@router.callback_query(F.data == "profile")
async def handle_profile(query: types.CallbackQuery) -> None:
    await profile_handler(query.message)


@router.callback_query(F.data == "progress")
async def handle_progress(query: types.CallbackQuery) -> None:
    await query.message.answer("Tu avance se mostrara aqui.")
    await query.answer()


@router.callback_query(F.data == "budget")
async def handle_budget(query: types.CallbackQuery) -> None:
    await query.message.answer("Budget disponible proximamente.")
    await query.answer()


@router.callback_query(F.data == "admin")
async def handle_admin(query: types.CallbackQuery) -> None:
    await query.message.answer("Menu de administracion")
    await query.answer()


@router.callback_query(F.data == "config")
async def handle_config(query: types.CallbackQuery) -> None:
    await query.message.answer("Opciones de configuracion")
    await query.answer()


@router.callback_query(F.data == "gamify")
async def handle_gamify(query: types.CallbackQuery) -> None:
    await query.message.answer("Opciones de gamificacion")
    await query.answer()
