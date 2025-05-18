"""logging_config.py — централизованная настройка логов проекта
==============================================================
Использование (однократно, например в `main.py`):

    import logging_config  # noqa: F401  # импорт сам вызывает setup()

Для явного вызова:

    import logging_config
    logging_config.setup()

Поведение:
  • Уровень логов зависит от settings.debug (DEBUG ⇔ INFO).
  • Логи всегда пишутся в файл `logs/bot.log` (RotatingFileHandler 5×5 MB).
  • В режиме debug дополнительно выводятся в консоль.
  • Формат: `YYYY-MM-DD HH:MM:SS | LEVEL | logger: message`.
"""
from __future__ import annotations

import logging
import logging.config
import os
from pathlib import Path
from typing import Any, Dict

from config import get_settings

# ───────────────────────────────────────────────────────────────
# Конструирование dictConfig
# ───────────────────────────────────────────────────────────────

def _build_dict_config(level: int, log_file: Path) -> Dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s | %(levelname)8s | %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": level,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "standard",
                "filename": str(log_file),
                "encoding": "utf8",
                "maxBytes": 5 * 1024 * 1024,  # 5 MB
                "backupCount": 5,
                "level": level,
            },
        },
        "root": {
            "handlers": ["file", "console"],
            "level": level,
        },
    }


# ───────────────────────────────────────────────────────────────
# Публичная функция setup()
# ───────────────────────────────────────────────────────────────

def setup(force: bool = False) -> None:
    """Настраивает logging; повторный вызов игнорируется, если `force`=False."""
    if logging.getLogger().handlers and not force:
        # Логирование уже сконфигурировано где‑то ещё.
        return

    settings = get_settings()

    # Каталог logs/
    log_dir = Path(os.getenv("LOG_DIR", "logs"))
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "bot.log"

    level = logging.DEBUG if settings.debug else logging.INFO

    logging.config.dictConfig(_build_dict_config(level, log_file))
    logging.getLogger(__name__).info("Logging initialized → %s (debug=%s)", log_file, settings.debug)


# ───────────────────────────────────────────────────────────────
# Автоматическая инициализация при импорте модуля
# ───────────────────────────────────────────────────────────────
setup()

__all__ = ["setup"]
