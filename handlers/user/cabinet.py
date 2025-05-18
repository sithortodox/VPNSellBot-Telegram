# handlers/user/cabinet.py
from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.user_kb import CallbackData, cabinet_menu_kb
from db.dao import get_balance

router = Router()


# ───────────────────────────────────────────
# Личный кабинет → показать подменю
# ───────────────────────────────────────────
@router.callback_query(lambda c: c.data == CallbackData.CABINET)
async def open_cabinet(callback: CallbackQuery) -> None:
    await callback.message.edit_reply_markup(reply_markup=cabinet_menu_kb())
    await callback.answer()  # убираем «часики» на кнопке


# ───────────────────────────────────────────
# История покупок / Мои конфиги (заглушка)
# ───────────────────────────────────────────
@router.callback_query(lambda c: c.data == CallbackData.CABINET_HISTORY)
async def show_history(callback: CallbackQuery) -> None:
    await callback.answer("📝 История покупок пока пуста.", show_alert=True)


# ───────────────────────────────────────────
# Мой баланс / Пополнить
# ───────────────────────────────────────────
@router.callback_query(lambda c: c.data == CallbackData.CABINET_BALANCE)
async def show_balance_topup(callback: CallbackQuery) -> None:
    bal = await get_balance(callback.from_user.id)
    await callback.answer()
    await callback.message.answer(f"💰 Ваш баланс: {bal}\n\nПополнение скоро будет доступно.")


# ───────────────────────────────────────────
# Реферальная программа (заглушка)
# ───────────────────────────────────────────
@router.callback_query(lambda c: c.data == CallbackData.CABINET_REFERRAL)
async def show_referral(callback: CallbackQuery) -> None:
    await callback.answer("👥 Реферальная программа в разработке…", show_alert=True)
