from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Mi perfil", callback_data="profile")],
        [InlineKeyboardButton(text="Recompensa diaria", callback_data="daily_reward")],
        [InlineKeyboardButton(text="Tarea semanal", callback_data="weekly_task")],
    ]
    if is_admin:
        buttons.append([InlineKeyboardButton(text="Panel admin", callback_data="admin")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_keyboard() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text="Usuarios", callback_data="admin_users")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
