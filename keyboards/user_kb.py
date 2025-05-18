"""
keyboards.user_kb — inline keyboards for user-facing menus.

Main menu:
  • 👤 Личный кабинет
  • 💰 Баланс
  • 🛠 Панель администратора (только для админов)

Cabinet submenu:
  • 📝 История покупок / Мои конфиги
  • 💰 Мой баланс / Пополнить
  • 👥 Реферальная программа
"""
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


__all__ = (
    "CallbackData",
    "main_menu_kb",
    "cabinet_menu_kb",
)


class CallbackData:
    """Centralised callback-data constants."""

    # Main menu
    CABINET = "cabinet"
    BALANCE = "balance"
    ADMIN_PANEL = "admin_panel"

    # Cabinet submenu
    CABINET_HISTORY = "cabinet:history"
    CABINET_BALANCE = "cabinet:balance"
    CABINET_REFERRAL = "cabinet:referral"


# ---------------------------------------------------------------------------
# Main menu keyboard
# ---------------------------------------------------------------------------

def main_menu_kb(is_admin: bool = False) -> InlineKeyboardMarkup:
    """Return inline keyboard for the main menu."""
    kb = InlineKeyboardBuilder()
    kb.button(text="👤 Личный кабинет", callback_data=CallbackData.CABINET)
    kb.button(text="💰 Баланс", callback_data=CallbackData.BALANCE)
    if is_admin:
        kb.button(text="🛠 Панель администратора", callback_data=CallbackData.ADMIN_PANEL)
    kb.adjust(1)
    return kb.as_markup()


# ---------------------------------------------------------------------------
# Cabinet submenu keyboard
# ---------------------------------------------------------------------------

def cabinet_menu_kb() -> InlineKeyboardMarkup:
    """Return inline keyboard for the cabinet submenu."""
    kb = InlineKeyboardBuilder()
    kb.button(
        text="📝 История покупок / Мои конфиги",
        callback_data=CallbackData.CABINET_HISTORY,
    )
    kb.button(
        text="💰 Мой баланс / Пополнить",
        callback_data=CallbackData.CABINET_BALANCE,
    )
    kb.button(
        text="👥 Реферальная программа",
        callback_data=CallbackData.CABINET_REFERRAL,
    )
    kb.adjust(1)
    return kb.as_markup()
