from aiogram import Router
from aiogram.filters import Command
from aiogram import types

from services.user_service import UserService
from services.point_service import PointService
from services.badge_service import BadgeService
from db import database

router = Router()
user_service = UserService()
point_service = PointService()
badge_service = BadgeService()


@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    user = await user_service.get_user_profile(message.from_user.id)
    if not user:
        await message.answer("Usuario no encontrado")
        return
    level_info = await point_service.calculate_level(user.get("points", 0))
    badges = await badge_service.get_user_badges(message.from_user.id)
    badges_text = ", ".join(b["name"] for b in badges) if badges else "Ninguna"
    level_name = level_info[1] if level_info else "-"
    text = (
        f"\ud83d\udc64 <b>{user.get('full_name')}</b>\n"
        f"Nivel: <b>{level_name}</b>\n"
        f"Puntos: <b>{user.get('points')}</b>\n"
        f"Presupuesto actual: <b>{user.get('current_budget')}</b>\n"
        f"Fecha de registro: <b>{user.get('join_date')}</b>\n"
        f"Insignias: {badges_text}"
    )
    await message.answer(text)


@router.message(Command("level"))
async def cmd_level(message: types.Message):
    user = await user_service.get_user_profile(message.from_user.id)
    if not user:
        await message.answer("Usuario no encontrado")
        return
    level = await point_service.calculate_level(user.get("points", 0))
    next_level = await database.get_next_level(user.get("points", 0))
    if next_level:
        progress = f"{user.get('points')}/{next_level['min_points']}"
    else:
        progress = "Maximo nivel"
    level_name = level[1] if level else "-"
    await message.answer(
        f"Nivel actual: <b>{level_name}</b>\nPuntos: {user.get('points')}\nProgreso: {progress}"
    )


@router.message(Command("badges"))
async def cmd_badges(message: types.Message):
    user_badges = await badge_service.get_user_badges(message.from_user.id)
    if not user_badges:
        await message.answer("A\u00fan no tienes insignias")
        return
    lines = [f"\u2022 {b['name']}" for b in user_badges]
    await message.answer("Insignias obtenidas:\n" + "\n".join(lines))


@router.message(Command("ranking"))
@router.message(Command("leaderboard"))
async def cmd_ranking(message: types.Message):
    top_users = await point_service.get_top_users(10)
    lines = []
    for idx, user in enumerate(top_users, start=1):
        name = user.get("full_name") or user.get("username") or user.get("user_id")
        lines.append(f"{idx}. {name} - {user.get('points')} pts")
    await message.answer("\uD83C\uDFC6 Ranking:\n" + "\n".join(lines))
