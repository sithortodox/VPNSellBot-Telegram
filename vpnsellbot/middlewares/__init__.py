"""
Пакет middleware для VPNSellBot.
Здесь собираются все кастомные middlewares.
"""

from .throttling import ThrottlingMiddleware

__all__ = [
    "ThrottlingMiddleware",
]
