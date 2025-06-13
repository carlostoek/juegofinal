from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import secrets

from services.user_service import list_users, remove_user

router = Router()


@router.message(Command("admin"))
async def admin_menu(message: types.Message) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Estad\u00edsticas", callback_data="admin_stats")],
            [InlineKeyboardButton(text="Broadcast", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="Generar link", callback_data="admin_token")],
            [InlineKeyboardButton(text="Suscriptores", callback_data="admin_subs")],
        ]
    )
    await message.answer("Administraci\u00f3n", reply_markup=keyboard)


@router.callback_query(F.data == "admin_stats")
async def admin_stats(query: types.CallbackQuery) -> None:
    users = await list_users()
    await query.message.answer(f"Total de usuarios: {len(users)}")
    await query.answer()


@router.callback_query(F.data == "admin_token")
async def admin_token(query: types.CallbackQuery) -> None:
    token = secrets.token_urlsafe(16)
    await query.message.answer(f"Link generado: https://t.me/tu_bot?start={token}")
    await query.answer()


@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(query: types.CallbackQuery) -> None:
    await query.message.answer("Env\u00eda el mensaje con /broadcast <texto>")
    await query.answer()


@router.message(Command("broadcast"))
async def broadcast_cmd(message: types.Message) -> None:
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        await message.answer("Uso: /broadcast <mensaje>")
        return
    text = parts[1]
    users = await list_users()
    for u in users:
        try:
            await message.bot.send_message(u.id, text)
        except Exception:
            pass
    await message.answer("Mensaje enviado.")


@router.callback_query(F.data == "admin_subs")
async def admin_subscribers(query: types.CallbackQuery) -> None:
    users = await list_users()
    if not users:
        await query.message.answer("Sin suscriptores.")
    for u in users:
        days = (datetime.utcnow() - u.join_date).days
        info = (
            f"{u.full_name} - Ingres\u00f3 {u.join_date.date()} - "+
            f"{days} d\u00edas - Renovaciones 0"
        )
        btn = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="Expulsar",
                    callback_data=f"expulsar:{u.id}")
            ]]
        )
        await query.message.answer(info, reply_markup=btn)
    await query.answer()


@router.callback_query(F.data.startswith("expulsar:"))
async def expulsar_callback(query: types.CallbackQuery) -> None:
    uid = int(query.data.split(":", 1)[1])
    await remove_user(uid)
    await query.message.answer(f"Usuario {uid} expulsado.")
    await query.answer()
