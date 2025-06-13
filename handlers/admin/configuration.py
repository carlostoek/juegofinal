from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from services.config_service import get_config, set_config

router = Router()


@router.message(Command("config"))
async def config_menu(message: types.Message) -> None:
    """Show configuration menu."""
    amount = await get_config("tariff_amount", "no establecido")
    period = await get_config("tariff_period", "0")
    text = f"Configuraci\u00f3n de tarifas actual: {amount} cada {period} d\u00edas"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Configurar tarifas", callback_data="cfg_tariff")],
        ]
    )
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "cfg_tariff")
async def cfg_tariff_callback(query: types.CallbackQuery) -> None:
    await query.message.answer(
        "Env\u00eda el comando /set_tarifa <monto> <dias> para establecer la tarifa"
    )
    await query.answer()


@router.message(Command("set_tarifa"))
async def set_tarifa(message: types.Message) -> None:
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Uso: /set_tarifa <monto> <dias>")
        return
    amount = parts[1]
    period = parts[2]
    await set_config("tariff_amount", amount)
    await set_config("tariff_period", period)
    await message.answer(f"Tarifa configurada en {amount} cada {period} d\u00edas")
