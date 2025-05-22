from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from vpnsellbot.config import get_settings
from vpnsellbot.db.dao import get_session
from vpnsellbot.db.models import User
from vpnsellbot.keyboards.user_kb import main_menu_keyboard

settings = get_settings()
router = Router(name="user_start")


@router.message(Command("start"))
async def start_handler(message: Message):
    """
    Обработчик команды /start.
    Регистрирует пользователя в БД (если новый) и показывает главное меню.
    """
    async with get_session() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            user = User(
                id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                is_admin=message.from_user.id in settings.admin_ids,
            )
            session.add(user)
            await session.commit()

    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n"
        "Это VPNSellBot. Выберите действие в меню ниже:",
        reply_markup=main_menu_keyboard(),
    )
