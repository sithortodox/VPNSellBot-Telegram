"""
Пакет пользовательских обработчиков VPNSellBot.
Импортирует и экспортирует все роутеры user-команд.
"""

from .start import router as start_router
from .balance import router as balance_router
from .cabinet import router as cabinet_router

__all__ = [
    "start_router",
    "balance_router",
    "cabinet_router",
]
