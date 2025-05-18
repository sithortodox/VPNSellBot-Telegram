# handlers/user/start.py
from aiogram import Router, F
from aiogram.types import Message

from config import get_settings
from db.dao import get_or_create_user
from keyboards.user_kb import main_menu_kb

router = Router()            # ← объявляем router ДО использования

@router.message(F.text == "/start")
async def cmd_start(message: Message) -> None:
    # регистрируем пользователя (если нового ещё нет)
    await get_or_create_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    settings = get_settings()
    is_admin = message.from_user.id in settings.admin_ids

    await message.answer(
        "👋 Добро пожаловать!",
        reply_markup=main_menu_kb(is_admin),
    )
