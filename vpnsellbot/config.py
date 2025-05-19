import os
from typing import Optional, List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    database_url: str = Field(..., env="DATABASE_URL")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    throttle_rate: float = Field(1.0, env="THROTTLE_RATE")
    admin_ids: List[int] = Field(..., env="ADMIN_IDS")
    default_page_size: int = Field(10, env="DEFAULT_PAGE_SIZE")

    class Config:
        # Загружать переменные из файла .env в корне проекта
        env_file = ".env"
        env_file_encoding = "utf-8"


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Возвращает единственный экземпляр настроек приложения.
    При первом вызове загружает их из окружения (.env).
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
