from dataclasses import dataclass
from datetime import date
from aiogram import Router, F
from aiogram.types import Message

# Placeholder user model
@dataclass
class User:
    id: int
    full_name: str
    level: int
    points: int
    join_date: date

# Placeholder database fetch function
async def get_user_from_db(user_id: int) -> User:
    # In a real application this would query the database
    # Here we return a dummy user for demonstration purposes
    return User(
        id=user_id,
        full_name="John Doe",
        level=1,
        points=0,
        join_date=date.today()
    )

router = Router()

@router.message(F.text == "/profile")
async def profile_handler(message: Message):
    user = await get_user_from_db(message.from_user.id)
    response = (
        f"Welcome {user.full_name}!\n"
        f"Level: {user.level}\n"
        f"Points: {user.points}\n"
        f"Joined: {user.join_date}"
    )
    await message.answer(response)
