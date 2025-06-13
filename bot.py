from aiogram import Bot, Dispatcher
from config import settings

from utils.logger import LoggingMiddleware, ErrorMiddleware

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
dp.update.middleware(LoggingMiddleware())
dp.update.middleware(ErrorMiddleware())
