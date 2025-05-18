"""handlers.user.cabinet.py — хэндлеры раздела «Личный кабинет».

Показывает подменю и заглушки для трёх пунктов:
  • История покупок / Мои конфиги
  • Мой баланс / Пополнить
  • Реферальная программа
"""
from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.user_kb import CallbackData, cabinet_menu_kb
from db.dao import get_balance

router = Router()

# -----------------------------------------------------------------------------
# Открыть подменю «Личный кабинет»
# -----------------------------------------------------------------------------
@router.callback_query(lambda c: c.data == CallbackData.CABINET)
async def open_cabinet(callback: CallbackQuery) -> None:
    """Заменяет клавиатуру на подменю кабинета."""
    await callback.message.edit_reply_markup(reply_markup=cabinet_menu_kb())
    await callback.answer()


# -----------------------------------------------------------------------------
# История покупок / Мои конфиги — заглушка
# -----------------------------------------------------------------------------
@router.callback_query(lambda c: c.data == CallbackData.CABINET_HISTORY)
async def show_history(callback: CallbackQuery) -> None:
    await callback.answer("📝 История покупок пока пуста.", show_alert=True)


# -----------------------------------------------------------------------------
# Мой баланс / Пополнить — показывает баланс, пополнение TBD
# -----------------------------------------------------------------------------
@router.callback_query(lambda c: c.data == CallbackData.CABINET_BALANCE)
async def show_balance_topup(callback: CallbackQuery) -> None:
    bal = await get_balance(callback.from_user.id)
    await callback.answer()
    await callback.message.answer(
        f"💰 Ваш баланс: {bal}\n\nПополнение будет доступно в ближайшем обновлении.")


# -----------------------------------------------------------------------------
# Реферальная программа — заглушка
# -----------------------------------------------------------------------------
@router.callback_query(lambda c: c.data == CallbackData.CABINET_REFERRAL)
async def show_referral(callback: CallbackQuery) -> None:
    await callback.answer("👥 Реферальная программа в разработке…", show_alert=True)


__all__ = ["router"]
