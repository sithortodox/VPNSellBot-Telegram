import pytest
from aiogram import Router

from vpnsellbot.handlers import (
    start_router,
    balance_router,
    cabinet_router,
    panel_router,
    add_balance_router,
    broadcast_router,
    statistics_router,
)

ALL_ROUTERS = [
    start_router,
    balance_router,
    cabinet_router,
    panel_router,
    add_balance_router,
    broadcast_router,
    statistics_router,
]


@pytest.mark.parametrize("router", ALL_ROUTERS)
def test_routers_are_router_instances(router):
    """
    Все экспортированные роутеры должны быть экземплярами aiogram.Router.
    """
    assert isinstance(router, Router), f"{router!r} is not a Router instance"
