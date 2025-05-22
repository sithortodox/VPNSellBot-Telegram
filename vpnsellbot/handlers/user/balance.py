from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from vpnsellbot.config import get_settings
from vpnsellbot.db.dao import get_session
from vpnsellbot.db.models import User
from vpnsellbot.keyboards.user_kb import main_menu_keyboard

settings = get_settings()
router = Router(name="user_balance")


@router.message(Command("balance"))
async def balance_handler(message: Message):
    """
    Обработчик команды /balance.
    Показывает текущий баланс пользователя.
    """
    async with get_session() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            # Если пользователь не зарегистрирован — предложим /start
            return await message.reply(
                "❗️ Вы не зарегистрированы. Пожалуйста, сначала отправьте /start."
            )

    # Отправляем баланс и возвращаем главное меню
    await message.answer(
        f"💰 Ваш текущий баланс: <b>{user.balance}</b>",
        reply_markup=main_menu_keyboard()
    )
