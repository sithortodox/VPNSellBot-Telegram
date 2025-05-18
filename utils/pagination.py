"""utils/pagination.py — простые утилиты разбиения коллекций на пачки
===================================================================
Зачем нужно:
  • Рассылки: отправлять сообщения батчами по 100 ID (лимит Telegram).
  • SQL IN (...) — делить большие списки, чтобы не превысить параметр
    max_bind_vars у PostgreSQL/SQLite.

Поддержка Python ≥3.8 (есть своя реализация, даже если itertools.batched нет).
"""
from __future__ import annotations

from collections.abc import AsyncIterator, Iterable, Iterator
from itertools import islice
from typing import List, Sequence, TypeVar

T = TypeVar("T")

# -----------------------------------------------------------------------------
# Синхронное разбиение
# -----------------------------------------------------------------------------

def chunked(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
    """Yield successive *size*-sized chunks from *iterable*.

    >>> list(chunked(range(7), 3))
    [[0, 1, 2], [3, 4, 5], [6]]
    """
    if size <= 0:
        raise ValueError("size must be > 0")

    it = iter(iterable)
    while (chunk := list(islice(it, size))):
        yield chunk


# -----------------------------------------------------------------------------
# Асинхронная версия (для aiogram broadcast)
# -----------------------------------------------------------------------------
async def achunked(aiterable: AsyncIterator[T], size: int) -> AsyncIterator[List[T]]:  # type: ignore  # noqa: ANN401
    """Асинхронно группирует элементы async-итератора в списки по *size*.

    Example:
        async for group in achunked(get_user_ids(), 100):
            ...
    """
    if size <= 0:
        raise ValueError("size must be > 0")

    batch: List[T] = []
    async for item in aiterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


# -----------------------------------------------------------------------------
# Helper: slice_sequence
# -----------------------------------------------------------------------------

def slice_sequence(seq: Sequence[T], size: int) -> List[Sequence[T]]:
    """Возвращает список срезов `seq[i:i+size]` (не копирует объекты)."""
    return [seq[i : i + size] for i in range(0, len(seq), size)]


__all__ = [
    "chunked",
    "achunked",
    "slice_sequence",
]
