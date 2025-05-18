# """keyboards/user\_kb.py — inline‑клавиатуры для пользователей

Главное меню: «Личный кабинет», «Баланс» и (для админов) «Панель администратора».
Подменю «Личный кабинет» содержит:
• История покупок / Мои конфиги
• Мой баланс / Пополнить
• Реферальная программа
"""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

**all** = \[
"CallbackData",
"main\_menu\_kb",
"cabinet\_menu\_kb",
]

# -----------------------------------------------------------------

# Callback data константы

# -----------------------------------------------------------------

class CallbackData:
\# Главное меню
CABINET = "cabinet"
BALANCE = "balance"       # остаётся для прямого вызова кнопки «Баланс»
ADMIN\_PANEL = "admin\_panel"

```
# Подменю личного кабинета
CABINET_HISTORY = "cabinet:history"
CABINET_BALANCE = "cabinet:balance"
CABINET_REFERRAL = "cabinet:referral"
```

# -----------------------------------------------------------------

# Главное меню

# -----------------------------------------------------------------

def main\_menu\_kb(is\_admin: bool = False) -> InlineKeyboardMarkup:
"""Inline‑меню первого уровня."""
kb = InlineKeyboardBuilder()

```
kb.button(text="👤 Личный кабинет", callback_data=CallbackData.CABINET)
kb.button(text="💰 Баланс", callback_data=CallbackData.BALANCE)

if is_admin:
    kb.button(text="🛠 Панель администратора", callback_data=CallbackData.ADMIN_PANEL)

kb.adjust(1)
return kb.as_markup()
```

# -----------------------------------------------------------------

# Подменю «Личный кабинет»

# -----------------------------------------------------------------

def cabinet\_menu\_kb() -> InlineKeyboardMarkup:
"""Возвращает клавиатуру раздела «Личный кабинет»."""
kb = InlineKeyboardBuilder()
kb.button(text="📝 История покупок / Мои конфиги", callback\_data=CallbackData.CABINET\_HISTORY)
kb.button(text="💰 Мой баланс / Пополнить", callback\_data=CallbackData.CABINET\_BALANCE)
kb.button(text="👥 Реферальная программа", callback\_data=CallbackData.CABINET\_REFERRAL)
kb.adjust(1)
return kb.as\_markup()
