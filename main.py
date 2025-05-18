"""main.py — точка входа Telegram‑бота ReputMail
================================================
Запускает бота в режиме polling (для Webhook см. TODO внизу).

• Инициализирует логирование (импорт logging_config)
• Загружает настройки из .env через config.py
• Создаёт Bot и Dispatcher (aiogram v3)
• Подключает middlewares (пример: ThrottlingMiddleware)
• Инклудит все рутеры из handlers/*
"""
from __future__ import annotations

import asyncio
import sys

# Настройка логов — импорт сам вызывает logging_config.setup()
import logging_config  # noqa: F401  pylint: disable=unused-import
from config import get_settings

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

# Middlewares (пример антиспам‑ограничений)
try:
    from middlewares.throttling import ThrottlingMiddleware  # noqa: WPS433
except ModuleNotFoundError:
    ThrottlingMiddleware = None  # type: ignore  # заглушка, если middleware ещё нет

dp = Dispatcher()

# Routers — импорты регистрируют команды/коллбэки
from handlers.user.cabinet import router as cabinet_router
dp.include_router(cabinet_router)
from handlers.user.start import router as start_router  # noqa: WPS433,E402
from handlers.user.balance import router as balance_router  # noqa: WPS433,E402
from handlers.admin.panel import router as admin_panel_router  # noqa: WPS433,E402
from handlers.admin.broadcast import router as broadcast_router  # noqa: WPS433,E402
from handlers.admin.add_balance import router as add_balance_router  # noqa: WPS433,E402
from handlers.admin.statistics import router as stats_router  # noqa: WPS433,E402

__all__ = ["run"]


async def run() -> None:  # pragma: no cover — точка входа
    settings = get_settings()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Подключаем middlewares, если они доступны
    if ThrottlingMiddleware:
        dp.message.middleware(ThrottlingMiddleware())
        dp.callback_query.middleware(ThrottlingMiddleware())

    # Подключаем все роутеры
    dp.include_router(start_router)
    dp.include_router(balance_router)
    dp.include_router(admin_panel_router)
    dp.include_router(broadcast_router)
    dp.include_router(add_balance_router)
    dp.include_router(stats_router)

    # Запуск long polling
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


# -----------------------------------------------------------------
# CLI‑старт via `python -m app.main` или `python main.py`
# -----------------------------------------------------------------
if __name__ == "__main__":
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

# TODO: Webhook‑режим (Gunicorn/Uvicorn) для продакшена
#   from aiohttp import web
#   async def on_startup(_: Bot):
#       await bot.set_webhook(settings.webhook_url)
#   web.run_app(dp.start_webhook(...))
