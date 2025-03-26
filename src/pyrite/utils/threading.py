from __future__ import annotations

from abc import ABC, abstractmethod
import asyncio
from collections.abc import Callable
import threading


class BaseThreader(ABC):

    @abstractmethod
    def start_thread(self, callable_: Callable, *args, **kwds) -> None: ...


class DefaultThreader(BaseThreader):
    def start_thread(self, callable: Callable, *args, **kwds) -> None:
        threading.Thread(target=callable, args=args, kwargs=kwds).start()


class AsyncThreader(BaseThreader):
    def start_thread(self, callable: Callable, *args, **kwds) -> None:
        asyncio.create_task(callable(*args, **kwds))


# Probably don't need classes for this, honestly just assigning two different functions
# would be sufficient.
active_threader = DefaultThreader()


def set_asyncio_mode():
    global active_threader
    active_threader = AsyncThreader()


def set_regular_mode():
    global active_threader
    active_threader = DefaultThreader()


def start_thread(callable: Callable, *args, **kwds) -> None:
    active_threader.start_thread(callable, *args, **kwds)
