import logging
import logging.config
import sys

# Конфигурация логирования
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
            "level": "DEBUG",  # Будет переопределён в setup_logging
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",  # Будет переопределён в setup_logging
    },
}


def setup_logging(log_level: str = "INFO") -> None:
    """
    Инициализирует конфигурацию логирования.
    Устанавливает уровень логирования для корневого логгера
    и консольного хэндлера в переданный log_level.
    """
    # Устанавливаем уровень для handler'а и корневого логгера
    LOGGING_CONFIG["handlers"]["console"]["level"] = log_level
    LOGGING_CONFIG["root"]["level"] = log_level

    # Применяем конфигурацию
    logging.config.dictConfig(LOGGING_CONFIG)
