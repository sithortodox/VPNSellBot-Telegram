import itertools
from typing import (
    Iterable,
    TypeVar,
    List,
    AsyncIterable,
    AsyncIterator,
)

T = TypeVar("T")


def chunked(iterable: Iterable[T], size: int) -> Iterable[List[T]]:
    """
    Разбивает синхронный итерируемый объект на чанки (списки) указанного размера.

    :param iterable: любой Iterable
    :param size: максимальный размер каждого чанка
    :return: генератор списков длиной до size
    """
    if size <= 0:
        raise ValueError("size must be positive")
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


async def achunked(aiterable: AsyncIterable[T], size: int) -> AsyncIterator[List[T]]:
    """
    Разбивает асинхронный итерируемый объект на чанки (списки) указанного размера.

    :param aiterable: любой AsyncIterable
    :param size: максимальный размер каждого чанка
    :return: асинхронный генератор списков длиной до size
    """
    if size <= 0:
        raise ValueError("size must be positive")
    buffer: List[T] = []
    async for item in aiterable:
        buffer.append(item)
        if len(buffer) >= size:
            yield buffer
            buffer = []
    if buffer:
        yield buffer
