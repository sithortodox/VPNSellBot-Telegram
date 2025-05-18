"""middlewares/throttling.py — антиспам middleware для aiogram v3
================================================================
Ограничивает частоту обработки апдейтов от одного пользователя.
По умолчанию: не чаще `limit=0.5` секунды (2 апдейта/сек).

Использование:
    from middlewares.throttling import ThrottlingMiddleware
    dp.message.middleware(ThrottlingMiddleware(limit=1.0))
    dp.callback_query.middleware(ThrottlingMiddleware(limit=0.5))

Для простоты хранит тайм‑штампы в памяти (словарь). В Kubernetes/
много‑процессной среде нужен Redis‑based throttling.
"""
from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import Any, Dict, MutableMapping

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from aiogram.exceptions import TelegramRetryAfter

__all__ = ["ThrottlingMiddleware"]


class ThrottlingMiddleware(BaseMiddleware):
    """Простой in‑memory throttling per user_id."""

    def __init__(self, limit: float = 0.5):
        self.limit = limit
        self._last_calls: MutableMapping[int, float] = {}
        self._lock = asyncio.Lock()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:  # noqa: D401, ANN401 — сигнатура BaseMiddleware
        user_id: int | None = None
        if isinstance(event, Message):
            user_id = event.from_user.id if event.from_user else None
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id if event.from_user else None

        if user_id is None:
            return await handler(event, data)

        async with self._lock:
            now = time.monotonic()
            last_time = self._last_calls.get(user_id, 0)
            delta = now - last_time
            if delta < self.limit:
                # Слишком быстро — игнорируем
                try:
                    if isinstance(event, CallbackQuery):
                        await event.answer("⏱ Подождите…", show_alert=False)
                    elif isinstance(event, Message):
                        await event.reply("⏱ Слишком быстро, подождите…", reply=False)
                except TelegramRetryAfter:  # flood‑контроль Telegram
                    pass
                return  # skip handler
            # Обновим таймштамп
            self._last_calls[user_id] = now

        return await handler(event, data)
