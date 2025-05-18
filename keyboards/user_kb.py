"""keyboards.user\_kb — inline keyboards for user-facing menus.

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

**all** = (
"CallbackData",
"main\_menu\_kb",
"cabinet\_menu\_kb",
)

class CallbackData:
"""Centralised callback-data constants."""

```
# Main menu
CABINET = "cabinet"
BALANCE = "balance"
ADMIN_PANEL = "admin_panel"

# Cabinet submenu
CABINET_HISTORY = "cabinet:history"
CABINET_BALANCE = "cabinet:balance"
CABINET_REFERRAL = "cabinet:referral"
```

# -----------------------------------------------------------------------------

# Main menu keyboard

# -----------------------------------------------------------------------------

def main\_menu\_kb(is\_admin: bool = False) -> InlineKeyboardMarkup:
"""Return inline keyboard for the main menu."""
kb = InlineKeyboardBuilder()
kb.button(text="👤 Личный кабинет", callback\_data=CallbackData.CABINET)
kb.button(text="💰 Баланс", callback\_data=CallbackData.BALANCE)
if is\_admin:
kb.button(text="🛠 Панель администратора", callback\_data=CallbackData.ADMIN\_PANEL)
kb.adjust(1)
return kb.as\_markup()

# -----------------------------------------------------------------------------

# Cabinet submenu keyboard

# -----------------------------------------------------------------------------

def cabinet\_menu\_kb() -> InlineKeyboardMarkup:
"""Return inline keyboard for the cabinet submenu."""
kb = InlineKeyboardBuilder()
kb.button(
text="📝 История покупок / Мои конфиги",
callback\_data=CallbackData.CABINET\_HISTORY,
)
kb.button(
text="💰 Мой баланс / Пополнить",
callback\_data=CallbackData.CABINET\_BALANCE,
)
kb.button(
text="👥 Реферальная программа",
callback\_data=CallbackData.CABINET\_REFERRAL,
)
kb.adjust(1)
return kb.as\_markup()
