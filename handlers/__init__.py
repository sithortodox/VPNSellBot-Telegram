from .user.start import router as start_router
from .user.balance import router as balance_router
from .user.cabinet import router as cabinet_router  # ← новое

__all__ = [
    "start_router",
    "balance_router",
    "cabinet_router",
]
