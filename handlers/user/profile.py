from aiogram import Router, F
from aiogram.types import Message

from utils import MSG

from services.user_service import get_user
from services.point_service import point_service
from services.badge_service import check_level_badges

router = Router()


def profile_text(user) -> str:
    points = point_service.get_points(str(user.id))
    level = point_service.get_level(str(user.id))
    rewards = point_service.get_rewards(str(user.id))
    budget = point_service.get_budget(str(user.id))
    return MSG.PROFILE.format(
        name=user.full_name,
        level=level,
        points=points,
        rewards=rewards,
        budget=budget,
        date=user.join_date.date(),
    )


@router.message(F.text == "/profile")
async def profile_handler(message: Message) -> None:
    user = await get_user(message.from_user.id)
    if user is None:
        await message.answer(MSG.NOT_REGISTERED)
        return
    level = point_service.get_level(str(user.id))
    await check_level_badges(user.id, level)
    response = profile_text(user)
    await message.answer(response)
