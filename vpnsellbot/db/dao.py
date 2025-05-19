import asyncio
from typing import Optional, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from vpnsellbot.config import get_settings
from vpnsellbot.db.models import Base

_engine: Optional[AsyncEngine] = None
_SessionMaker: Optional[sessionmaker] = None


def init_engine(database_url: str) -> None:
    """
    Инициализирует глобальный AsyncEngine и SessionMaker для работы с БД.
    """
    global _engine, _SessionMaker
    if _engine is None:
        _engine = create_async_engine(database_url, echo=False, future=True)
        _SessionMaker = sessionmaker(
            _engine, expire_on_commit=False, class_=AsyncSession
        )


def get_engine() -> AsyncEngine:
    """
    Возвращает единственный экземпляр AsyncEngine, создавая его при необходимости.
    """
    if _engine is None:
        settings = get_settings()
        init_engine(settings.database_url)
    return _engine


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор для сессии SQLAlchemy.
    Использование:
        async for session in get_session():
            ...
    или
        async with get_session() as session:
            ...
    """
    assert _SessionMaker is not None, "Session maker is not initialized"
    async with _SessionMaker() as session:
        yield session


async def create_schema() -> None:
    """
    Создаёт в базе все таблицы, описанные в metadata моделей.
    """
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
