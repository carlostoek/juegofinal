from aiogram import Router

from .start_menu import router as start_menu_router
from .profile_commands import router as profile_router


def register_handlers() -> Router:
    router = Router()
    router.include_router(start_menu_router)
    router.include_router(profile_router)
    return router
