from aiogram import Router, types
from aiogram.filters import Command

from config import ADMIN_IDS
from services.purchase_service import PurchaseService
from services.point_service import PointService
from services.mission_service import MissionService

router = Router()
purchase_service = PurchaseService()
point_service = PointService()
mission_service = MissionService()


@router.message(Command("sumarpuntos"))
async def cmd_sumarpuntos(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Uso: /sumarpuntos [ID_usuario] [monto_MXN]")
        return
    try:
        user_id = int(parts[1])
        amount = float(parts[2])
    except ValueError:
        await message.answer("Valores invalidos")
        return
    await purchase_service.record_purchase(user_id, amount)
    await purchase_service.award_purchase_points(user_id, amount)
    await purchase_service.check_bonus_purchases(user_id)
    await message.answer("Compra registrada y puntos otorgados")


@router.message(Command("crearmision"))
async def cmd_crear_mision(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    parts = message.text.split(maxsplit=6)
    if len(parts) < 7:
        await message.answer("Uso: /crearmision tipo descripcion puntos criterio desde hasta")
        return
    _, m_type, desc, points, criteria, active_from, active_until = parts
    mission_id = await mission_service.create_mission(m_type, desc, int(points), criteria, active_from, active_until)
    await message.answer(f"Mision creada ID {mission_id}")


@router.message(Command("activarmision"))
async def cmd_activar_mision(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Uso: /activarmision [ID]")
        return
    mission_id = int(parts[1])
    await mission_service.activate_mission(mission_id)
    await message.answer("Mision activada")
