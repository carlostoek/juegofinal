from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from utils import MSG

from services.poll_service import poll_service
from config import settings

router = Router()


@router.message(Command("poll"))
async def send_poll(message: types.Message) -> None:
    """Create a simple yes/no poll."""
    poll = await message.answer_poll(
        question=MSG.POLL_QUESTION,
        options=["Si", "No"],
        is_anonymous=False,
    )
    poll_service.add_poll(poll.poll.id, poll.message_id)

    # Offer button to close the poll for admins
    if message.from_user.id in settings.admin_ids:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="Cerrar encuesta",
                    callback_data=f"close_poll:{poll.poll.id}",
                )
            ]]
        )
        await message.answer(MSG.POLL_ADMIN, reply_markup=keyboard)


@router.callback_query(F.data.startswith("close_poll:"))
async def close_poll(query: CallbackQuery) -> None:
    """Allow admins to close a poll."""
    poll_id = query.data.split(":", 1)[1]
    message_id = poll_service.get_message_id(poll_id)
    if message_id is None:
        await query.answer(MSG.POLL_NOT_FOUND, show_alert=True)
        return

    await query.bot.stop_poll(chat_id=query.message.chat.id, message_id=message_id)
    poll_service.remove_poll(poll_id)
    await query.message.answer(MSG.POLL_CLOSED)
    await query.answer()
