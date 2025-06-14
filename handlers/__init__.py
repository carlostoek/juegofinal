from aiogram import Router

from .start import router as start_router


def register_handlers() -> Router:
    router = Router()
    router.include_router(start_router)
    return router
