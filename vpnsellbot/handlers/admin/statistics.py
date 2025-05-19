from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import select, func

from vpnsellbot.config import get_settings
from vpnsellbot.db.dao import get_session
from vpnsellbot.db.models import User, BalanceTransaction, Subscription

settings = get_settings()
router = Router(name="admin_statistics")


@router.message(
    Command("statistics"),
    F.from_user.id.in_(settings.admin_ids)
)
async def statistics(message: Message):
    """
    Отправляет администратору общую статистику по боту:
      - число пользователей
      - суммарный баланс
      - число транзакций
      - общее и активных подписок
    """
    async with get_session() as session:
        # Общее число пользователей
        total_users = await session.scalar(
            select(func.count()).select_from(User)
        )

        # Суммарный баланс всех пользователей
        total_balance = await session.scalar(
            select(func.coalesce(func.sum(User.balance), 0))
        )

        # Всего транзакций пополнения
        total_transactions = await session.scalar(
            select(func.count()).select_from(BalanceTransaction)
        )

        # Всего подписок и активных
        total_subscriptions = await session.scalar(
            select(func.count()).select_from(Subscription)
        )
        active_subscriptions = await session.scalar(
            select(func.count()).select_from(Subscription).where(Subscription.active.is_(True))
        )

    # Формируем ответ
    text = (
        f"📊 <b>Статистика бота</b>\n\n"
        f"👤 Пользователей: <b>{total_users}</b>\n"
        f"💰 Общий баланс: <b>{total_balance}</b>\n"
        f"🧾 Транзакций пополнения: <b>{total_transactions}</b>\n"
        f"🔔 Подписок всего: <b>{total_subscriptions}</b>\n"
        f"✅ Активных подписок: <b>{active_subscriptions}</b>"
    )

    await message.reply(text)
