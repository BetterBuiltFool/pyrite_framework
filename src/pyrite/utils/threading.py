from __future__ import annotations

from abc import ABC, abstractmethod
import asyncio
from collections.abc import Callable
import threading


class BaseThreader(ABC):
    """
    Base class for the threading system.

    Has one method, start_thread, which is called from the module level.
    """

    @abstractmethod
    def start_thread(self, callable_: Callable, *args, **kwds) -> None: ...


class DefaultThreader(BaseThreader):
    """
    Standard threader that uses the regular threading module.
    Use for non-web compatible deployments.
    """

    def start_thread(self, callable: Callable, *args, **kwds) -> None:
        threading.Thread(target=callable, args=args, kwargs=kwds).start()


class AsyncThreader(BaseThreader):
    """
    Variant threader that uses asyncio green threads. Use this for web-based deployment.
    """

    def start_thread(self, callable: Callable, *args, **kwds) -> None:
        asyncio.create_task(callable(*args, **kwds))


# Probably don't need classes for this, honestly just assigning two different functions
# would be sufficient.
_active_threader = DefaultThreader()


def _set_asyncio_mode():
    """
    Sets the threader to an async-aware threader.
    """
    global _active_threader
    _active_threader = AsyncThreader()


def _set_regular_mode():
    """
    Sets the threader to a standard threader.
    """
    global _active_threader
    _active_threader = DefaultThreader()


def start_thread(callable: Callable, *args, **kwds) -> None:
    """
    Starts a thread using the current threading system.
    The threading system is determined by the game type.

    When in asyncio mode, callables must be async aware.

    :param callable: The callable or coroutine being started by the threader.
    """
    _active_threader.start_thread(callable, *args, **kwds)
