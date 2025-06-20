import logging
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from config import BOT_TOKEN
from handlers import register_handlers
from middlewares.logging_middleware import LoggingMiddleware
from db.database import init_db
from cron_jobs import (
    Scheduler,
    daily_reset_interaction_limit,
    award_permanence_points_job,
    check_and_award_missions,
    finalize_auctions_job,
    run_monthly_raffle,
    run_weekly_mini_raffle,
    update_weekly_activity_ranking,
)


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "errors.log"),
        logging.StreamHandler(),
    ],
)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.update.middleware(LoggingMiddleware())
scheduler = Scheduler()


def register_all_handlers() -> None:
    dp.include_router(register_handlers())


async def on_startup(bot: Bot) -> None:
    await init_db()
    scheduler.add_daily_job(daily_reset_interaction_limit)
    scheduler.add_daily_job(award_permanence_points_job)
    scheduler.add_daily_job(check_and_award_missions)
    scheduler.add_daily_job(finalize_auctions_job)
    scheduler.add_daily_job(run_monthly_raffle)
    scheduler.add_daily_job(run_weekly_mini_raffle)
    scheduler.add_daily_job(update_weekly_activity_ranking)
    dp.loop.create_task(scheduler.start(bot))
    logging.info("Bot started")


async def on_shutdown(bot: Bot) -> None:
    logging.info("Bot shutdown")


if __name__ == "__main__":
    register_all_handlers()
    dp.run_polling(bot, on_startup=on_startup, on_shutdown=on_shutdown)
