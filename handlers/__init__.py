from aiogram import Router

from .start_menu import router as start_menu_router


def register_handlers() -> Router:
    router = Router()
    router.include_router(start_menu_router)
    return router
