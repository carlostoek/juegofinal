from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text="Perfil", callback_data="profile")]]
    if is_admin:
        buttons.append([InlineKeyboardButton(text="Panel admin", callback_data="admin")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_keyboard() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text="Usuarios", callback_data="admin_users")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
