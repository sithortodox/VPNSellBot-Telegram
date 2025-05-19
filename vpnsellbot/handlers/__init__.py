"""
VPNSellBot handlers package initializer.
Collects all routers for including in Dispatcher.
"""

# User handlers
from .user.start import router as start_router
from .user.balance import router as balance_router
from .user.cabinet import router as cabinet_router

# Admin handlers
from .admin.panel import router as panel_router
from .admin.add_balance import router as add_balance_router
from .admin.broadcast import router as broadcast_router
from .admin.statistics import router as statistics_router

__all__ = [
    # user
    "start_router",
    "balance_router",
    "cabinet_router",
    # admin
    "panel_router",
    "add_balance_router",
    "broadcast_router",
    "statistics_router",
]
