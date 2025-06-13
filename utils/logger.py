import logging
import traceback
from pathlib import Path
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


# Ensure logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
ERROR_LOG_FILE = LOG_DIR / "errors.log"

# Configure root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console output for all logs
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

# Error file handler
error_file_handler = logging.FileHandler(ERROR_LOG_FILE)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(error_file_handler)


class LoggingMiddleware(BaseMiddleware):
    """Middleware that logs incoming updates and exceptions."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        logger.info("Incoming update: %s", event)
        try:
            return await handler(event, data)
        except Exception:  # pragma: no cover - runtime safeguard
            tb = traceback.format_exc()
            logger.error("Exception occurred while handling update:\n%s", tb)
            # Also write traceback to error log for persistence
            with ERROR_LOG_FILE.open("a") as f:
                f.write(tb + "\n")
            raise
