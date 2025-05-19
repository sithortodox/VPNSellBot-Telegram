"""
Пакет admin-обработчиков VPNSellBot.
Импортирует и экспортирует все роутеры админ-команд.
"""

from .add_balance import router as add_balance_router
from .broadcast import router as broadcast_router
from .panel import router as panel_router
from .statistics import router as statistics_router

__all__ = [
    "add_balance_router",
    "broadcast_router",
    "panel_router",
    "statistics_router",
]
