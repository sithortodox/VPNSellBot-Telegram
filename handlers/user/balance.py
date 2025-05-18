from aiogram import Router
from aiogram.types import CallbackQuery
from db.dao import get_balance
from keyboards.user_kb import CallbackData

router = Router()

@router.callback_query(lambda c: c.data == CallbackData.BALANCE)
async def show_balance(callback: CallbackQuery) -> None:
    bal = await get_balance(callback.from_user.id)
    await callback.answer()
    await callback.message.answer(f"💰 Ваш баланс: {bal}")
