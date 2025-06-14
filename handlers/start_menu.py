from aiogram import Router
from aiogram.filters import Command
from aiogram import types

from services.user_service import UserService
from services.point_service import PointService
from services.badge_service import BadgeService
from services.daily_reward_service import DailyRewardService
from services.mission_service import MissionService
from utils.keyboards import start_keyboard

router = Router()
user_service = UserService()
point_service = PointService()
badge_service = BadgeService()
daily_reward_service = DailyRewardService()
mission_service = MissionService()


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


@router.callback_query(lambda c: c.data == "profile")
async def cb_profile(callback: types.CallbackQuery):
    user = await user_service.get_user_profile(callback.from_user.id)
    if not user:
        await callback.message.answer("Usuario no encontrado")
        await callback.answer()
        return
    level_info = await point_service.calculate_level(user.get("points", 0))
    badges = await badge_service.get_user_badges(callback.from_user.id)
    badges_text = ", ".join(b["name"] for b in badges) if badges else "Ninguna"
    level_name = level_info[1] if level_info else "-"
    text = (
        f"\U0001F464 <b>{user.get('full_name')}</b>\n"
        f"Nivel: <b>{level_name}</b>\n"
        f"Puntos: <b>{user.get('points')}</b>\n"
        f"Presupuesto actual: <b>{user.get('current_budget')}</b>\n"
        f"Fecha de registro: <b>{user.get('join_date')}</b>\n"
        f"Insignias: {badges_text}"
    )
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(lambda c: c.data == "daily_reward")
async def cb_daily_reward(callback: types.CallbackQuery):
    claimed = await daily_reward_service.claim_reward(callback.from_user.id)
    if claimed:
        await callback.message.answer("Has recibido 10 puntos de recompensa diaria!")
    else:
        await callback.answer("Ya reclamaste tu recompensa hoy", show_alert=True)
        return
    await callback.answer()


@router.callback_query(lambda c: c.data == "weekly_task")
async def cb_weekly_task(callback: types.CallbackQuery):
    mission = await mission_service.get_active_mission()
    if not mission:
        await callback.message.answer("No hay tarea semanal activa")
    else:
        desc = mission.get("description")
        pts = mission.get("points_reward")
        await callback.message.answer(f"Tarea semanal: {desc}\nRecompensa: {pts} puntos")
    await callback.answer()
