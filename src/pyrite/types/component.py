from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, TypeVar
from weakref import WeakKeyDictionary

if TYPE_CHECKING:
    from typing import Any, Self

T = TypeVar("T", bound="Component")


class Component(ABC):
    instances: WeakKeyDictionary[Any, Component] = WeakKeyDictionary()

    def __init_subclass__(cls: type[T]) -> None:
        cls.instances: WeakKeyDictionary[Any, T] = WeakKeyDictionary()

    def __new__(cls: type[T], owner: Any, *args, **kwds) -> Self:
        new_component = super().__new__(cls)
        cls.instances.update({owner: new_component})
        return new_component
