import logging
from pathlib import Path
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
ERROR_LOG_FILE = LOG_DIR / "errors.log"

logger = logging.getLogger("bot")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    error_file_handler = logging.FileHandler(ERROR_LOG_FILE)
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    logger.addHandler(error_file_handler)


class LoggingMiddleware(BaseMiddleware):
    """Log every incoming update."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        logger.info("Incoming update: %s", event)
        return await handler(event, data)


class ErrorMiddleware(BaseMiddleware):
    """Catch exceptions and log tracebacks."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception:  # pragma: no cover - runtime safeguard
            logger.exception("Exception while handling update")
            raise
