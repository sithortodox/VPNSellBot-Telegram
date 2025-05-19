from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from vpnsellbot.config import get_settings

settings = get_settings()
router = Router(name="admin_panel")


@router.message(
    Command("panel"),
    F.from_user.id.in_(settings.admin_ids)
)
async def panel(message: Message):
    """
    Отображает админ-панель с основными командами:
      - /add_balance
      - /broadcast
      - /statistics
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/add_balance"), KeyboardButton(text="/broadcast")],
            [KeyboardButton(text="/statistics")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.reply(
        "🔧 <b>Админ-панель</b>\nВыберите действие:",
        reply_markup=keyboard
    )
