from sqlalchemy import select

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from vpnsellbot.config import get_settings
from vpnsellbot.db.dao import get_session
from vpnsellbot.db.models import User

settings = get_settings()
router = Router(name="admin_broadcast")


@router.message(
    Command("broadcast"),
    F.from_user.id.in_(settings.admin_ids)
)
async def broadcast(message: Message):
    """
    Команда администратора для массовой рассылки.
    Использование: /broadcast <текст сообщения>
    """
    # Получаем текст после команды
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        return await message.reply(
            "❗️ Неверный синтаксис.\n"
            "Использование: /broadcast <текст сообщения>"
        )
    text = parts[1].strip()

    # Получаем всех пользователей из БД
    async with get_session() as session:
        result = await session.execute(select(User.id))
        user_ids = [row[0] for row in result.all()]

    # Рассылаем сообщение каждому
    success_count = 0
    fail_count = 0

    for user_id in user_ids:
        try:
            await message.bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode="HTML"
            )
            success_count += 1
        except Exception:
            fail_count += 1

    # Отчёт админу
    await message.reply(
        f"✅ Рассылка завершена.\n"
        f"Успешно отправлено: <b>{success_count}</b>\n"
        f"Не удалось отправить: <b>{fail_count}</b>"
    )
