from __future__ import annotations

from abc import ABC, abstractmethod
import asyncio
from collections.abc import Callable
import threading


class BaseThreader(ABC):

    @abstractmethod
    def start_thread(self, callable_: Callable, *args) -> None: ...


class DefaultThreader(BaseThreader):
    def start_thread(self, callable_: Callable, *args) -> None:
        threading.Thread(target=callable_, args=args).start()


class AsyncThreader(BaseThreader):
    def start_thread(self, callable_: Callable, *args) -> None:
        asyncio.create_task(callable_(*args))
