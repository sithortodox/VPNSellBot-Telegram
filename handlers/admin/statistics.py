from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.user_kb import CallbackData

router = Router()

@router.callback_query(lambda c: c.data == CallbackData.ADMIN_PANEL + ":stats")
async def admin_stats(callback: CallbackQuery) -> None:
    await callback.answer("📊 Статистика в разработке…", show_alert=True)
