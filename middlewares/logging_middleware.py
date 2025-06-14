import logging
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        logging.info(f"Update: {event}")
        try:
            return await handler(event, data)
        except Exception as e:
            logging.exception("Error while processing update")
            raise e
