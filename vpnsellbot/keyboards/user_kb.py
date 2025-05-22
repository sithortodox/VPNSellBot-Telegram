from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData as BaseCallbackData


class CallbackData(BaseCallbackData, prefix="vpnsell"):
    """
    Универсальный CallbackData для inline-кнопок в боте.
    Поле `action` описывает действие, поле `target` — необязательный целевой идентификатор.
    """
    action: str
    target: int | None = None  # например, ID записи для пагинации или детального просмотра


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Возвращает ReplyKeyboardMarkup с основным меню пользователя:
      - /balance — просмотр баланса
      - /cabinet — личный кабинет
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/balance"), KeyboardButton(text="/cabinet")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
