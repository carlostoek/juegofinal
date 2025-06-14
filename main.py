import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import register_handlers
from middlewares.logging_middleware import LoggingMiddleware
from db.database import init_db
from cron_jobs import (
    Scheduler,
    daily_reset_interaction_limit,
    award_permanence_points_job,
    check_and_award_missions,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/errors.log"),
        logging.StreamHandler()
    ]
)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
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
    dp.loop.create_task(scheduler.start(bot))
    logging.info("Bot started")


async def on_shutdown(bot: Bot) -> None:
    logging.info("Bot shutdown")


if __name__ == "__main__":
    register_all_handlers()
    dp.run_polling(bot, on_startup=on_startup, on_shutdown=on_shutdown)
