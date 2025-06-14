from aiogram import Router, types
from aiogram.filters import Command
import aiosqlite
from db.database import DB_PATH

from services.reward_service import RewardService
from services.auction_service import AuctionService
from services.daily_gift_service import DailyGiftService

router = Router()
reward_service = RewardService()
auction_service = AuctionService()
daily_gift_service = DailyGiftService()


@router.message(Command("catalogo"))
async def cmd_catalogo(message: types.Message):
    rewards = await reward_service.get_all_rewards()
    if not rewards:
        await message.answer("No hay recompensas disponibles")
        return
    lines = [f"{r['reward_id']}. {r['name']} - {r['cost_points']} pts" for r in rewards]
    await message.answer("Catalogo de recompensas:\n" + "\n".join(lines))


@router.message(Command("canjear"))
async def cmd_canjear(message: types.Message, bot):
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Uso: /canjear [ID_recompensa]")
        return
    reward_id = int(parts[1])
    success = await reward_service.redeem_reward(message.from_user.id, reward_id)
    if not success:
        await message.answer("No tienes puntos suficientes o recompensa invalida")
        return
    await reward_service.deliver_reward(message.from_user.id, reward_id, bot)
    await message.answer("Recompensa canjeada")


@router.message(Command("pujar"))
async def cmd_pujar(message: types.Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Uso: /pujar [cantidad_puntos]")
        return
    bid = int(parts[1])
    async with aiosqlite.connect(str(DB_PATH)) as db:
        cur = await db.execute(
            "SELECT auction_id FROM auctions WHERE status='active' ORDER BY start_time LIMIT 1"
        )
        row = await cur.fetchone()
        if not row:
            await message.answer("No hay subastas activas")
            return
        auction_id = row[0]
    success = await auction_service.place_bid(auction_id, message.from_user.id, bid)
    if success:
        await message.answer("Puja registrada")
    else:
        await message.answer("Puja no v\u00e1lida")


@router.message(Command("regalodiario"))
async def cmd_regalodiario(message: types.Message, bot):
    gift = await daily_gift_service.get_current_daily_gift()
    if not gift:
        await message.answer("No hay regalo hoy")
        return
    if await daily_gift_service.has_claimed_today(message.from_user.id):
        await message.answer("Ya reclamaste el regalo de hoy")
        return
    info = await daily_gift_service.claim_gift(message.from_user.id, gift["gift_id"])
    if not info:
        await message.answer("Error al reclamar")
        return
    if info["gift_type"] == "text" and info["content"]:
        await bot.send_message(message.from_user.id, info["content"])
    await message.answer("Regalo obtenido")
