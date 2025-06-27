from __future__ import annotations

from typing import Self, TYPE_CHECKING, TypeVar
from weakref import ref, WeakKeyDictionary

if TYPE_CHECKING:
    from typing import Any

T = TypeVar("T", bound="Component")


class Component:
    """
    Components are objects that mark other object with attributes. Components can be
    intersected with other components to get a set of shared key objects.
    """

    def __init_subclass__(cls) -> None:
        cls.instances: WeakKeyDictionary[Any, Self] = WeakKeyDictionary()

    def __new__(cls, owner: Any, *args, **kwds):
        new_component = super().__new__(cls)
        cls.instances.update({owner: new_component})
        return new_component

    def __init__(self, owner: Any) -> None:
        self._owner = ref(owner)

    @property
    def owner(self) -> Any:
        """
        The owning object for the component.
        Property returns a strong reference.
        """
        return self._owner()

    @classmethod
    def intersect(cls, *component_types: type[T]) -> set[Any]:
        """
        Generates a set of keys that are shared between the component and the supplied
        component types. Can take any number of component types.

        :component_types: Any number of component classes.
        :return: A set of objects that exist as keys for all involved components.
        """

        key_sets = (
            set(component_type.instances.keys()) for component_type in component_types
        )
        local_keys = set(cls.instances.keys())
        return local_keys.intersection(*key_sets)

    @classmethod
    def get(cls: type[T], key: Any) -> T:
        """
        Returns the component instance belonging to the key.

        :param key: The owning object of a component.
        :return: The component instance belonging to _key_, if extantit exists
        """
        return cls.get_instances()[key]

    @classmethod
    def keys(cls) -> set[Any]:
        return set(cls.instances.keys())

    @classmethod
    def remove_from(cls, key: Any):
        """
        Removes the component instance belonging to _key_, if it exists.

        :param key: The owning object of a component.
        """
        component = cls.instances.pop(key, None)
        if component is not None:
            cls._purge_component(component)

    @classmethod
    def _purge_component(cls, component: T):
        """
        Method for cleaning up a component's data when the component is used.
        If the data is simple, a weak key dictionary with the components as keys may be
        sufficient, but for complex data storage (i.e. numpy arrays as storage), it may
        be necessary to implement this for a subclass.

        :param component: The component instance to be purged.
        """
        pass

    @classmethod
    def get_instances(cls: type[T]) -> dict[Any, T]:
        """
        Gives a dictionary of all component instances and their owners.

        :return: The component's instance collection, as a dictionary.
        """
        return cls.instances
