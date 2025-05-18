from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.user_kb import CallbackData

router = Router()

@router.callback_query(lambda c: c.data == CallbackData.ADMIN_PANEL + ":broadcast")
async def admin_broadcast(callback: CallbackQuery) -> None:
    await callback.answer("📢 Функция рассылки в разработке…", show_alert=True)
