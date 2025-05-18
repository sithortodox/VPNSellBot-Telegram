from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.user_kb import CallbackData, main_menu_kb

router = Router()

@router.callback_query(lambda c: c.data == CallbackData.ADMIN_PANEL)
async def admin_panel(callback: CallbackQuery) -> None:
    await callback.answer("🛠 Функция в разработке…", show_alert=True)
