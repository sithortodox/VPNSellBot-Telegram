"""config.py — централизованная загрузка настроек проекта
====================================================
⚙️ Использует python‑dotenv для чтения переменных окружения.

Обязательно задайте в .env:
    BOT_TOKEN=<telegram token>
    ADMIN_IDS=123456789,987654321   # через запятую

Опционально:
    DATABASE_URL=postgresql+asyncpg://user:pass@host/db  # по умолчанию SQLite
    DEBUG=true                                          # логирование DEBUG
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Set

from dotenv import load_dotenv

# ───────────────────────────────────────────────────────────────
# Модель настроек
# ───────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    database_url: str
    admin_ids: Set[int]
    debug: bool = False


# ───────────────────────────────────────────────────────────────
# Вспомогательные функции
# ───────────────────────────────────────────────────────────────

def _parse_admin_ids(raw: str | None) -> Set[int]:
    if not raw:
        return set()
    return {int(x) for x in raw.split(',') if x.strip()}


# ───────────────────────────────────────────────────────────────
# Публичная точка входа
# ───────────────────────────────────────────────────────────────

def load_settings() -> Settings:
    """Читает .env и возвращает экземпляр Settings."""
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("BOT_TOKEN не найден в переменных окружения (.env)")

    database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///data.db")
    admin_ids = _parse_admin_ids(os.getenv("ADMIN_IDS"))
    debug_flag = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes"}

    return Settings(
        bot_token=bot_token,
        database_url=database_url,
        admin_ids=admin_ids,
        debug=debug_flag,
    )


# ───────────────────────────────────────────────────────────────
# Глобальный объект настроек (lazy‑load при импорте)
# ───────────────────────────────────────────────────────────────
settings: Settings | None = None


def get_settings() -> Settings:
    global settings  # pylint: disable=global-statement
    if settings is None:
        settings = load_settings()
    return settings


__all__ = [
    "Settings",
    "load_settings",
    "get_settings",
]
