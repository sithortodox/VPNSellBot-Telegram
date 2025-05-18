"""keyboards/user_kb.py — inline‑клавиатуры для пользователей
===========================================================
Создаёт главное меню (Service X, Balance). При флаге `is_admin=True`
добавляет кнопку «Admin Panel» — чтобы не дублировать код.
"""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

__all__ = [
    "CallbackData",
    "main_menu_kb",
]

# -----------------------------------------------------------------
# Callback data константы (используются в handlers)
# -----------------------------------------------------------------

class CallbackData:
    SERVICE_X = "service_x"
    BALANCE = "balance"
    ADMIN_PANEL = "admin_panel"


# -----------------------------------------------------------------
# Конструктор клавиатуры
# -----------------------------------------------------------------

def main_menu_kb(is_admin: bool = False) -> InlineKeyboardMarkup:
    """Возвращает InlineKeyboardMarkup главного меню."""
    kb = InlineKeyboardBuilder()

    kb.button(text="⚙️ Service X", callback_data=CallbackData.SERVICE_X)
    kb.button(text="💰 Balance", callback_data=CallbackData.BALANCE)

    if is_admin:
        kb.button(text="🛠 Admin Panel", callback_data=CallbackData.ADMIN_PANEL)

    kb.adjust(1)  # по одной кнопке в строке
    return kb.as_markup()
