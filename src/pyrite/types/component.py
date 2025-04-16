from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, TypeVar
from weakref import ref, WeakKeyDictionary

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
        new_component._owner = ref(owner)
        return new_component

    @property
    def owner(self) -> Any:
        return self._owner()

    @classmethod
    def intersection(cls, *component_types: type[T]) -> dict[Any, tuple[type[T], ...]]:
        """
        Creates a dictionary of all components with shared owners.

        :return: _description_
        """
        # Outputs a dictionary with a key and tuple of component instances,
        # such that for each component within, component.owner = key
        intersection = {
            key: tuple(component[key] for component in component_types)
            for key in cls.get_shared_keys(*component_types)
        }
        return intersection

    @classmethod
    def get_shared_keys(cls, *component_types: type[T]) -> set[Any]:
        """
        Generates a set of keys that are shared between the component and the supplied
        component types. Can take any number of component types.

        :component_types: Any number of component classes.
        :return: A set of objects that exist as keys for all involved components.
        """
        key_sets = (
            set(component_type.instances.keys()) for component_type in component_types
        )
        return set(cls.instances.keys()).intersection(key_sets)

    @classmethod
    def get_instances(cls: type[T]) -> dict[Any, T]:
        """
        Gives a dictionary of all component instances and their owners.

        :return: The component's instance collection, as a dictionary.
        """
        return cls.instances
