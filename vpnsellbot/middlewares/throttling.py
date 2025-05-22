import time
import asyncio
from typing import Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramRetryAfter


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware для защиты от флуда.
    Блокирует повторные запросы от одного пользователя, пока не истечёт указанный интервал.
    """

    def __init__(self, rate: float = 1.0):
        """
        :param rate: минимальный интервал в секундах между двумя обновлениями от одного пользователя
        """
        super().__init__()
        self.rate = rate
        self._last_calls: dict[int, float] = {}
        self._lock = asyncio.Lock()

    async def __call__(self, handler, event, data):
        # Определяем user_id для разных типов update
        user_id: int | None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            # для остальных апдейтов не применяем throttling
            return await handler(event, data)

        now = time.monotonic()
        # Всю работу с кэшем оборачиваем через Lock, чтобы избежать race condition
        async with self._lock:
            last = self._last_calls.get(user_id)
            if last is not None and (now - last) < self.rate:
                # Если пользователь слишком быстро шлёт запросы — отправляем уведомление
                try:
                    if isinstance(event, Message):
                        await event.reply(
                            f"⏳ Пожалуйста, подождите {self.rate:.1f} сек. между командами."
                        )
                    else:  # CallbackQuery
                        await event.message.answer(
                            f"⏳ Пожалуйста, подождите {self.rate:.1f} сек. между действиями."
                        )
                except Exception:
                    # Игнорируем любые ошибки при уведомлении
                    pass
                return  # не вызываем handler — сбрасываем запрос

            # Ставим отметку о последнем успешном запросе
            self._last_calls[user_id] = now

        # Вызываем следующий обработчик
        try:
            return await handler(event, data)
        except TelegramRetryAfter:
            # Если Telegram попросил повторить через некоторое время — ничего не делаем
            return
