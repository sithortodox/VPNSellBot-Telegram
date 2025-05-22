import os
import asyncio

import pytest

from vpnsellbot.main import main


@pytest.fixture(autouse=True)
def env_vars(monkeypatch):
    """
    Подставляем тестовые переменные окружения,
    чтобы get_settings() корректно грузил конфиг.
    """
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("THROTTLE_RATE", "0.1")
    monkeypatch.setenv("ADMIN_IDS", "1,2,3")
    monkeypatch.setenv("DEFAULT_PAGE_SIZE", "5")


@pytest.mark.asyncio
async def test_main_is_coroutine_function():
    """
    Проверяем, что main — это coroutine function.
    """
    assert asyncio.iscoroutinefunction(main)


@pytest.mark.asyncio
async def test_main_runs_without_errors(monkeypatch):
    """
    Пробегаемся по основному потоку запуска бота,
    подменяя Bot, Dispatcher и инициализацию БД,
    чтобы убедиться, что main() не падает.
    """
    # Заглушки для Bot и Dispatcher
    class DummyBot:
        def __init__(self, *args, **kwargs):
            pass

    class DummyDispatcher:
        def __init__(self, storage=None):
            # эмуляция middleware API
            class Upd:
                def middleware(self, mw):
                    pass

            self.update = Upd()

        def include_router(self, router):
            # проверяем, что передаём объекты-роутеры
            assert hasattr(router, "message") or hasattr(router, "callback_query")

        async def start_polling(self, bot):
            # сразу выходим, чтобы не вешаться в вечном лонгпулле
            return

    # Подставляем заглушки вместо реальных классов и функций
    monkeypatch.setattr("vpnsellbot.main.Bot", DummyBot)
    monkeypatch.setattr("vpnsellbot.main.Dispatcher", DummyDispatcher)
    monkeypatch.setattr("vpnsellbot.db.dao.init_engine", lambda url: None)
    monkeypatch.setattr(
        "vpnsellbot.db.dao.create_schema", lambda: asyncio.sleep(0)
    )

    # Запускаем main() и убеждаемся, что он завершится без исключений
    await asyncio.wait_for(main(), timeout=1)
