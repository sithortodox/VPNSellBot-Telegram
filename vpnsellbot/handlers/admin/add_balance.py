from decimal import Decimal, InvalidOperation

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from vpnsellbot.config import get_settings
from vpnsellbot.db.dao import get_session
from vpnsellbot.db.models import User, BalanceTransaction

settings = get_settings()
router = Router(name="admin_add_balance")


@router.message(
    Command("add_balance"),
    F.from_user.id.in_(settings.admin_ids)
)
async def add_balance(message: Message):
    """
    Команда администратора для пополнения баланса пользователя.
    Использование: /add_balance <user_id> <amount>
    """
    parts = message.text.strip().split()
    if len(parts) != 3:
        return await message.reply(
            "❗️ Неверный синтаксис.\n"
            "Использование: /add_balance <user_id> <amount>"
        )

    _, user_id_str, amount_str = parts

    # Валидируем user_id
    try:
        user_id = int(user_id_str)
    except ValueError:
        return await message.reply("❗️ Неверный формат user_id. Должно быть целое число.")

    # Валидируем сумму
    try:
        amount = Decimal(amount_str)
    except InvalidOperation:
        return await message.reply("❗️ Неверный формат суммы. Используйте число, например 100.50")

    # Проводим операцию в базе
    async with get_session() as session:
        user = await session.get(User, user_id)
        if not user:
            return await message.reply(f"❗️ Пользователь с ID {user_id} не найден.")

        # Обновляем баланс
        user.balance += amount

        # Записываем транзакцию
        tx = BalanceTransaction(
            user_id=user_id,
            amount=amount,
            description=f"Пополнение админом {message.from_user.id}"
        )
        session.add(tx)

        await session.commit()
        await session.refresh(user)

    # Ответ админу
    await message.reply(
        f"✅ Баланс пользователя <b>{user_id}</b> успешно обновлён.\n"
        f"Новый баланс: <b>{user.balance}</b>"
    )
