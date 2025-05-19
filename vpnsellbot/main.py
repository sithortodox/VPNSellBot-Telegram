import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from vpnsellbot.config import get_settings
from vpnsellbot.logging_config import setup_logging
from vpnsellbot.db.dao import init_engine, create_schema
from vpnsellbot.middlewares.throttling import ThrottlingMiddleware

# User handlers
from vpnsellbot.handlers.user.start import router as start_router
from vpnsellbot.handlers.user.balance import router as balance_router
from vpnsellbot.handlers.user.cabinet import router as cabinet_router

# Admin handlers
from vpnsellbot.handlers.admin.panel import router as panel_router
from vpnsellbot.handlers.admin.add_balance import router as add_balance_router
from vpnsellbot.handlers.admin.broadcast import router as broadcast_router
from vpnsellbot.handlers.admin.statistics import router as statistics_router


async def main():
    # Load settings and initialize logging
    settings = get_settings()
    setup_logging(settings.log_level)

    logging.getLogger(__name__).info("Starting VPNSellBot...")

    # Initialize database connection and create tables
    init_engine(settings.database_url)
    await create_schema()

    # Initialize bot and dispatcher
    bot = Bot(token=settings.telegram_bot_token, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # Register throttling middleware for all updates
    dp.update.middleware(ThrottlingMiddleware(rate=settings.throttle_rate))

    # Include all routers
    for router in (
        start_router,
        balance_router,
        cabinet_router,
        panel_router,
        add_balance_router,
        broadcast_router,
        statistics_router,
    ):
        dp.include_router(router)

    # Start long-polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
