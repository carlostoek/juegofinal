from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

from utils import MSG

from services.reaction_service import reaction_service

router = Router()


@router.message(Command("feedback"))
async def send_feedback(message: Message) -> None:
    """Send a message with inline reaction buttons."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="\U0001F44D", callback_data="react_up"),
                InlineKeyboardButton(text="\U0001F44E", callback_data="react_down"),
            ]
        ]
    )
    await message.answer(MSG.FEEDBACK_QUESTION, reply_markup=keyboard)


@router.callback_query(F.data.in_("react_up", "react_down"))
async def handle_reaction(query: CallbackQuery) -> None:
    """Update reaction counts and acknowledge the user."""
    if query.message:
        message_id = query.message.message_id
        reaction = "\U0001F44D" if query.data == "react_up" else "\U0001F44E"
        reaction_service.add_reaction(message_id, reaction)
        counts = reaction_service.get_counts(message_id)
        await query.answer(f"\U0001F44D {counts['\U0001F44D']}  \U0001F44E {counts['\U0001F44E']}")
    else:
        await query.answer()
