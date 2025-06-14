from aiogram import Router, types
from aiogram.filters import Command

from config import ADMIN_IDS
from services.reaction_service import ReactionService
from services.poll_service import PollService


router = Router()
reaction_service = ReactionService()
poll_service = PollService()


@router.message(Command("feedback"))
async def cmd_feedback(message: types.Message):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="🔥", callback_data="reaction_🔥"),
                types.InlineKeyboardButton(text="👍", callback_data="reaction_👍"),
            ]
        ]
    )
    await message.answer("Deja tu reacci\u00f3n", reply_markup=kb)


@router.callback_query(lambda c: c.data and c.data.startswith("reaction_"))
async def handle_reaction(callback: types.CallbackQuery):
    reaction = callback.data.split("_")[1]
    user_id = callback.from_user.id
    can = await reaction_service.can_react_today(user_id)
    if not can:
        await callback.answer("L\u00edmite diario alcanzado", show_alert=True)
        return
    await reaction_service.record_reaction(callback.message.message_id, user_id, reaction)
    await reaction_service.award_reaction_points(user_id)
    await callback.answer("\u2705 Registrado")


@router.message(Command("poll"))
async def cmd_poll(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Debes proporcionar la pregunta")
        return
    question = parts[1]
    poll_id = await poll_service.create_poll(question, message.from_user.id)
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="S\u00ed", callback_data=f"poll_yes_{poll_id}"),
                types.InlineKeyboardButton(text="No", callback_data=f"poll_no_{poll_id}"),
            ],
            [
                types.InlineKeyboardButton(text="Cerrar encuesta", callback_data=f"close_poll_{poll_id}")
            ],
        ]
    )
    sent = await message.answer(question, reply_markup=kb)
    await poll_service.update_poll_message_id(poll_id, sent.message_id)


@router.callback_query(lambda c: c.data and (c.data.startswith("poll_yes_") or c.data.startswith("poll_no_")))
async def handle_poll_vote(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    vote = parts[1]
    poll_id = int(parts[2])
    recorded = await poll_service.record_vote(poll_id, callback.from_user.id, vote)
    if not recorded:
        await callback.answer("Ya has votado o la encuesta est\u00e1 cerrada", show_alert=True)
        return
    await poll_service.award_poll_points(callback.from_user.id)
    await callback.answer("Voto registrado")


@router.callback_query(lambda c: c.data and c.data.startswith("close_poll_"))
async def handle_close_poll(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer()
        return
    poll_id = int(callback.data.split("_")[2])
    await poll_service.deactivate_poll(poll_id)
    results = await poll_service.get_poll_results(poll_id)
    if results:
        yes_count, no_count = results
        text = f"Resultados: S\u00ed {yes_count} - No {no_count}"
    else:
        text = "Sin resultados"
    await callback.message.edit_reply_markup()
    await callback.message.answer(text)
    await callback.answer("Encuesta cerrada")

