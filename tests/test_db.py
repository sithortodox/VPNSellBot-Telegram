import os
import asyncio

import pytest
from sqlalchemy import inspect

from vpnsellbot.config import get_settings
from vpnsellbot.db.dao import init_engine, get_engine, get_session, create_schema
from vpnsellbot.db.models import Base, User, BalanceTransaction, Subscription


@pytest.fixture(autouse=True)
def env_vars(monkeypatch):
    """
    Подставляем тестовые переменные окружения для in-memory SQLite.
    """
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("THROTTLE_RATE", "0.1")
    monkeypatch.setenv("ADMIN_IDS", "1,2,3")
    monkeypatch.setenv("DEFAULT_PAGE_SIZE", "5")


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_engine_and_session_setup():
    """
    Проверяем, что init_engine и get_engine создают AsyncEngine,
    а get_session выдаёт AsyncSession.
    """
    settings = get_settings()
    # Инициализируем движок
    init_engine(settings.database_url)
    engine = get_engine()
    assert engine is not None, "Engine должен быть инициализирован"
    # Сессия должна быть асинхронным генератором
    sess_gen = get_session()
    assert hasattr(sess_gen, "__aiter__"), "get_session должен возвращать AsyncGenerator"


@pytest.mark.asyncio
async def test_create_schema_and_crud():
    """
    Проверяем, что create_schema создаёт таблицы, и
    что мы можем создать, прочитать и удалить запись User.
    """
    # Инициализируем и создаём схему
    settings = get_settings()
    init_engine(settings.database_url)
    await create_schema()

    # Проверяем, что таблицы появились
    engine = get_engine()
    insp = inspect(engine.sync_engine)
    tables = insp.get_table_names()
    assert "users" in tables
    assert "balance_transactions" in tables
    assert "subscriptions" in tables

    # CRUD: создаём пользователя, транзакцию и подписку
    async with get_session() as session:
        # Создаём пользователя
        user = User(
            id=42,
            username="testuser",
            first_name="Test",
            last_name="User",
            is_admin=False,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        assert user.id == 42
        assert user.username == "testuser"

        # Создаём транзакцию баланса
        tx = BalanceTransaction(
            user_id=user.id,
            amount=100.50,
            description="Test top-up"
        )
        session.add(tx)
        await session.commit()
        # Проверяем, что транзакция связана с пользователем
        await session.refresh(user)
        assert len(user.transactions) == 1
        assert float(user.transactions[0].amount) == 100.50

        # Создаём подписку
        sub = Subscription(
            user_id=user.id,
            plan="TestPlan",
            start_at="2025-01-01 00:00:00",
            end_at="2025-02-01 00:00:00",
            active=True
        )
        session.add(sub)
        await session.commit()
        await session.refresh(user)
        assert len(user.subscriptions) == 1
        assert user.subscriptions[0].plan == "TestPlan"

        # Удаляем пользователя — каскадно удалятся связанные записи
        await session.delete(user)
        await session.commit()

    # После удаления таблицы пусты
    async with get_session() as session:
        count_users = await session.scalar(
            Base.metadata.tables["users"].count()
        )
        assert count_users == 0
