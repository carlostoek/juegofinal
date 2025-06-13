from aiogram import Bot, Dispatcher
from config import settings
from utils.logger import LoggingMiddleware

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
dp.update.middleware(LoggingMiddleware())

