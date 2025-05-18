"""keyboards/user\_kb.py — inline keyboards for user-facing menus.

Main menu:
• 👤 Личный кабинет
• 💰 Баланс
• 🛠 Панель администратора (только для админов)

Cabinet submenu:
• 📝 История покупок / Мои конфиги
• 💰 Мой баланс / Пополнить
• 👥 Реферальная программа
"""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

**all** = (
"CallbackData",
"main\_menu\_kb",
"cabinet\_menu\_kb",
)

class CallbackData:
"""Callback-data constants used across handlers."""

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

# -----------------------------------------------------------------

# Main menu keyboard

# -----------------------------------------------------------------

def main\_menu\_kb(is\_admin: bool = False) -> InlineKeyboardMarkup:
"""Return inline keyboard for the main menu."""
builder = InlineKeyboardBuilder()
builder.button(text="👤 Личный кабинет", callback\_data=CallbackData.CABINET)
builder.button(text="💰 Баланс", callback\_data=CallbackData.BALANCE)
if is\_admin:
builder.button(text="🛠 Панель администратора", callback\_data=CallbackData.ADMIN\_PANEL)
builder.adjust(1)
return builder.as\_markup()

# -----------------------------------------------------------------

# Cabinet submenu keyboard

# -----------------------------------------------------------------

def cabinet\_menu\_kb() -> InlineKeyboardMarkup:
"""Return inline keyboard for the cabinet submenu."""
builder = InlineKeyboardBuilder()
builder.button(
text="📝 История покупок / Мои конфиги",
callback\_data=CallbackData.CABINET\_HISTORY,
)
builder.button(
text="💰 Мой баланс / Пополнить",
callback\_data=CallbackData.CABINET\_BALANCE,
)
builder.button(
text="👥 Реферальная программа",
callback\_data=CallbackData.CABINET\_REFERRAL,
)
builder.adjust(1)
return builder.as\_markup()
