"""db/dao.py — асинхронный слой доступа к данным (DAO)
=====================================================
Работает поверх SQLAlchemy 2.0 async.

Типовые задачи:
  • Инициализация движка и сессии (`init_engine`)
  • CRUD‑операции с `User` и логами
  • Транзакционная смена баланса с записью в `BalanceLog`
"""
from __future__ import annotations

import contextlib
from decimal import Decimal
from typing import AsyncGenerator, Iterable, List

from sqlalchemy import Select, func, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from config import get_settings
from db.models import BalanceLog, Base, BroadcastLog, User

# ───────────────────────────────────────────────────────────────
# Engine & Session
# ───────────────────────────────────────────────────────────────
_settings = get_settings()

_engine: AsyncEngine = create_async_engine(
    _settings.database_url,
    echo=_settings.debug,
    pool_pre_ping=True,
)
_SessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=_engine,
    expire_on_commit=False,
)

# ───────────────────────────────────────────────────────────────
# Helper context manager
# ───────────────────────────────────────────────────────────────
@contextlib.asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный context manager with‑session pattern."""
    async with _SessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:  # noqa: BLE001 — перекатываем rollback для любой ошибки
            await session.rollback()
            raise

# ───────────────────────────────────────────────────────────────
# Schema management (dev‑only)
# ───────────────────────────────────────────────────────────────
async def create_schema() -> None:
    """Создаёт все таблицы (используйте только в dev или тестах)."""
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ───────────────────────────────────────────────────────────────
# User helpers
# ───────────────────────────────────────────────────────────────
async def get_or_create_user(tg_id: int, username: str | None = None,
                             first_name: str | None = None,
                             last_name: str | None = None) -> User:
    async with session_scope() as session:
        stmt: Select[tuple[User]] = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user: User | None = result.scalar_one_or_none()
        if user:
            return user

        user = User(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        session.add(user)
        await session.flush()
        return user


async def get_balance(tg_id: int) -> Decimal:
    async with session_scope() as session:
        stmt: Select[tuple[Decimal]] = select(User.balance).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        balance = result.scalar_one()
        if balance is None:
            raise NoResultFound(f"User {tg_id} not found")
        return balance


async def update_balance(admin_id: int, tg_id: int, delta: Decimal) -> Decimal:
    """Смещение баланса на delta и запись в BalanceLog. Возвращает новый баланс."""
    async with session_scope() as session:
        # SELECT FOR UPDATE
        stmt = select(User).where(User.tg_id == tg_id).with_for_update()
        user: User = (await session.execute(stmt)).scalar_one()

        before = user.balance
        user.balance += delta
        after = user.balance

        session.add(
            BalanceLog(
                admin_id=admin_id,
                user_id=tg_id,
                delta=delta,
                before=before,
                after=after,
            )
        )
        return after


# ───────────────────────────────────────────────────────────────
# Broadcast helpers
# ───────────────────────────────────────────────────────────────
async def create_broadcast_log(author_id: int, text: str) -> int:
    async with session_scope() as session:
        log = BroadcastLog(author_id=author_id, text=text)
        session.add(log)
        await session.flush()  # гарантирует наличие log.id
        return log.id


async def update_broadcast_stats(log_id: int, sent_total: int, errors: int) -> None:
    async with session_scope() as session:
        stmt = (
            update(BroadcastLog)
            .where(BroadcastLog.id == log_id)
            .values(sent_total=sent_total, errors=errors, finished_at=func.now())
        )
        await session.execute(stmt)


# ───────────────────────────────────────────────────────────────
# Utility selects
# ───────────────────────────────────────────────────────────────
async def list_all_user_ids() -> List[int]:
    async with session_scope() as session:
        result = await session.execute(select(User.tg_id))
        return [row[0] for row in result.all()]


async def count_users(active_since: None | str = None) -> int:
    """Пример статистики: общее число пользователей (можно добавить фильтр)."""
    async with session_scope() as session:
        stmt = select(func.count()).select_from(User)
        result = await session.execute(stmt)
        return int(result.scalar_one())


__all__ = [
    "create_schema",
    "get_or_create_user",
    "get_balance",
    "update_balance",
    "create_broadcast_log",
    "update_broadcast_stats",
    "list_all_user_ids",
    "count_users",
]
