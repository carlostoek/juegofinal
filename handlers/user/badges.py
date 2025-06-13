from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "/badges")
async def badges_handler(message: Message) -> None:
 codex/commit-badge-system-and-/badges-command-changes
    badges = point_service.get_badges(str(message.from_user.id))
    if badges:
        lines = "\n".join(f"\U0001F396 {b}" for b in badges)
        await message.answer(f"Your badges:\n{lines}")
    else:
        await message.answer("You have no badges yet. Keep earning points!")
