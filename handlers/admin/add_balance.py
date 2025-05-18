from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.user_kb import CallbackData

router = Router()

@router.callback_query(lambda c: c.data == CallbackData.ADMIN_PANEL + ":add_balance")
async def admin_add_balance(callback: CallbackQuery) -> None:
    await callback.answer("💸 Начисление баланса в разработке…", show_alert=True)
