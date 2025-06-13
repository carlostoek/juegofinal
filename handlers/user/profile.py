from aiogram import Router, F
from aiogram.types import Message

from services.user_service import get_user
from services.point_service import point_service

router = Router()


@router.message(F.text == "/profile")
async def profile_handler(message: Message) -> None:
    user = await get_user(message.from_user.id)
    if user is None:
        await message.answer("You are not registered. Use /start first.")
        return

    points = point_service.get_points(str(user.id))
    level = point_service.get_level(str(user.id))
    rewards = point_service.get_rewards(str(user.id))
    budget = point_service.get_budget(str(user.id))

    response = (
        f"\u2728 Perfil de {user.full_name} \u2728\n"
        f"Nivel: {level}\n"
        f"Puntos: {points}\n"
        f"Recompensas: {rewards}\n"
        f"Budget: {budget}\n"
        f"Unido: {user.join_date.date()}"
    )
    await message.answer(response)
