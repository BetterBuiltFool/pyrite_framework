from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any, Self
    from weakref import WeakKeyDictionary


class Component(ABC):
    """
    Components are objects that mark other object with attributes. Components can be
    intersected with other components to get a set of shared key objects.
    """

    instances: WeakKeyDictionary[Any, Self]

    @property
    @abstractmethod
    def owner(self) -> Any:
        """
        The owning object for the component.
        Property returns a strong reference.
        """
        ...

    @classmethod
    @abstractmethod
    def intersect(cls, *component_types: type[Component]) -> set[Any]:
        """
        Generates a set of keys that are shared between the component and the supplied
        component types. Can take any number of component types.

        :component_types: Any number of component classes.
        :return: A set of objects that exist as keys for all involved components.
        """
        ...

    @classmethod
    @abstractmethod
    def get(cls, key: Any) -> Self | None:
        """
        Returns the component instance belonging to the key.

        :param key: The owning object of a component.
        :return: The component instance belonging to _key_, if extantit exists
        """
        ...

    @classmethod
    @abstractmethod
    def keys(cls) -> set[Any]: ...

    @classmethod
    @abstractmethod
    def remove_from(cls, key: Any):
        """
        Removes the component instance belonging to _key_, if it exists.

        :param key: The owning object of a component.
        """
        ...

    @classmethod
    @abstractmethod
    def get_instances(cls) -> Mapping[Any, Self]:
        """
        Gives a dictionary of all component instances and their owners.

        :return: The component's instance collection, as a dictionary.
        """
        ...
