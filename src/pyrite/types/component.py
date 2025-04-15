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

    @classmethod
    def intersection(cls, *component_types: type[T]) -> dict[Any, tuple[type[T], ...]]:
        intersection = {
            key: tuple(component[key] for component in component_types)
            for key in cls.get_shared_keys(*component_types)
        }
        return intersection

    @classmethod
    def get_shared_keys(cls, *component_types: type[T]) -> set[Any]:
        key_sets = (
            set(component_type.instances.keys()) for component_type in component_types
        )
        return set(cls.instances.keys()).intersection(key_sets)

    @classmethod
    def get_instances(cls: type[T]) -> dict[Any, T]:
        return cls.instances
