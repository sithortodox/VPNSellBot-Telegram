"""db/models.py — ORM‑модели SQLAlchemy 2.0 для ReputMail Bot
===========================================================
• Минимальные таблицы: users, broadcast_logs, balance_logs.
• Поддерживает любые БД (SQLite для dev, PostgreSQL для prod).
• Для асинхронной работы используйте `create_async_engine` в db/dao.py.
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, MetaData, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ───────────────────────────────────────────────────────────────
# MetaData с красивыми именами ограничений (Alembic-friendly)
# ───────────────────────────────────────────────────────────────
_convention = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=_convention)


class Base(DeclarativeBase):
    """Базовый класс declarative‑моделей."""

    metadata = metadata
    type_annotation_map = {Decimal: Numeric(14, 2)}  # глобальный маппинг


# ───────────────────────────────────────────────────────────────
# Таблица пользователей
# ───────────────────────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[str | None] = mapped_column(String(32))
    first_name: Mapped[str | None] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(64))
    balance: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User id={self.id} tg_id={self.tg_id} balance={self.balance}>"


# ───────────────────────────────────────────────────────────────
# Лог рассылок
# ───────────────────────────────────────────────────────────────
class BroadcastLog(Base):
    __tablename__ = "broadcast_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    sent_total: Mapped[int] = mapped_column(Integer, default=0)
    errors: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


# ───────────────────────────────────────────────────────────────
# Лог операций с балансом
# ───────────────────────────────────────────────────────────────
class BalanceLog(Base):
    __tablename__ = "balance_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    admin_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delta: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    before: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    after: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


__all__ = [
    "Base",
    "metadata",
    "User",
    "BroadcastLog",
    "BalanceLog",
]
