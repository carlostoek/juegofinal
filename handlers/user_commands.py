from aiogram import Router, types
from aiogram.filters import Command

from services.reward_service import RewardService

router = Router()
reward_service = RewardService()


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
