from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import select, desc

from vpnsellbot.config import get_settings
from vpnsellbot.db.dao import get_session
from vpnsellbot.db.models import User, BalanceTransaction, Subscription
from vpnsellbot.keyboards.user_kb import main_menu_keyboard

settings = get_settings()
router = Router(name="user_cabinet")


@router.message(Command("cabinet"))
async def cabinet_handler(message: Message):
    """
    Обработчик команды /cabinet.
    Показывает последние транзакции и подписки пользователя.
    """
    user_id = message.from_user.id

    async with get_session() as session:
        user = await session.get(User, user_id)
        if not user:
            # Если пользователь не зарегистрирован — предложим /start
            return await message.reply(
                "❗️ Вы не зарегистрированы. Пожалуйста, сначала отправьте /start."
            )

        # Получаем последние транзакции
        tx_stmt = (
            select(BalanceTransaction)
            .where(BalanceTransaction.user_id == user_id)
            .order_by(desc(BalanceTransaction.created_at))
            .limit(settings.default_page_size)
        )
        tx_result = await session.execute(tx_stmt)
        transactions = tx_result.scalars().all()

        # Получаем последние подписки
        sub_stmt = (
            select(Subscription)
            .where(Subscription.user_id == user_id)
            .order_by(desc(Subscription.created_at))
            .limit(settings.default_page_size)
        )
        sub_result = await session.execute(sub_stmt)
        subscriptions = sub_result.scalars().all()

    # Формируем текст ответа
    lines = [f"👤 <b>Личный кабинет</b> — {user.first_name}\n"]

    # Транзакции
    lines.append("💳 <b>Последние пополнения:</b>")
    if transactions:
        for tx in transactions:
            ts = tx.created_at.strftime("%Y-%m-%d %H:%M")
            amt = tx.amount
            desc = tx.description or ""
            lines.append(f"{ts} — +{amt} {desc}")
    else:
        lines.append("Нет операций пополнения.")

    # Подписки
    lines.append("\n🔔 <b>Последние подписки:</b>")
    if subscriptions:
        for sub in subscriptions:
            start = sub.start_at.strftime("%Y-%m-%d")
            end = sub.end_at.strftime("%Y-%m-%d")
            status = "✅ Активна" if sub.active else "❌ Неактивна"
            lines.append(f"{sub.plan}: {start} → {end} ({status})")
    else:
        lines.append("Нет подписок.")

    text = "\n".join(lines)

    await message.answer(text, reply_markup=main_menu_keyboard())
