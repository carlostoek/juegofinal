from aiogram import Router

from .start_menu import router as start_menu_router
from .profile_commands import router as profile_router
from .interaction_handlers import router as interaction_router
from .admin_commands import router as admin_router
from .user_commands import router as user_cmd_router


def register_handlers() -> Router:
    router = Router()
    router.include_router(start_menu_router)
    router.include_router(profile_router)
    router.include_router(interaction_router)
    router.include_router(admin_router)
    router.include_router(user_cmd_router)
    return router
