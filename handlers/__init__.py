from .user.start import router as start_router
from .user.balance import router as balance_router
from .admin.panel import router as admin_panel_router

__all__ = [
    "start_router",
    "balance_router",
    "admin_panel_router",
]
