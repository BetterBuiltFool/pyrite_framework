from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, TypeVar
from weakref import WeakKeyDictionary

if TYPE_CHECKING:
    from typing import Any

T = TypeVar("T", bound="Component")


class Component(ABC):
    instances: WeakKeyDictionary[Any, Component] = WeakKeyDictionary()

    def __init_subclass__(cls: type[T]) -> None:
        cls.instances: WeakKeyDictionary[Any, T] = WeakKeyDictionary()
