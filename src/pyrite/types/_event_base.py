from __future__ import annotations

from abc import ABC
from collections.abc import Callable
from typing import cast, TypeVar
from weakref import ref, WeakKeyDictionary


T = TypeVar("T", bound="HasEvents")
E = TypeVar("E", bound="InstanceEvent")


class InstanceEvent(ABC):
    instances: WeakKeyDictionary[T, InstanceEvent] = WeakKeyDictionary()

    def __init__(self, instance: T) -> None:
        self.instance = ref(instance)
        """
        Adds a reference to the owning instance, in case the event requires it.
        """
        self.listeners = set()
        """
        A set containing all listeners for this event instance.
        TODO Make a WeakSet? Otherwise may try and call dead functions.
        TODO Add a set for listeners that are non-static methods.
        """

    def __init_subclass__(cls) -> None:
        # Using a WeakKeyDictionary since we only need the instance if the
        # HasEvents instance is still around. We don't need to keep hold on the
        # HasEvents instance.
        cls.instances = WeakKeyDictionary()

    def _register(self, listener: Callable):
        self.listeners.add(listener)

    def _deregister(self, listener: Callable):
        self.listeners.discard(listener)

    def _notify(self, *args, **kwds):
        """
        Calls all registered listeners, passing along the args and kwds.
        This is never called directly, the instance event subclass will have its own
        defined call method that defines its parameters, which are passed on to the
        listeners.
        TODO Add threading/async support options.
        """
        for listener in self.listeners:
            listener(*args, **kwds)


class HasEvents(ABC):
    def __init__(self) -> None:
        self.events: dict[type[InstanceEvent], InstanceEvent] = {}

    def add_listener(self, event_type: type[E]) -> Callable:
        """
        Adds a function, method, or other callable to the InstanceEvent's listeners.
        That listener will be called whenever the event is fired.
        TODO make this able to accept non-static methods.

        :param event_type: The type of the event being set up.
        :return: The original listener, to be available for reuse.
        """

        def decorator(listener: Callable) -> Callable:
            self._register(event_type, listener)
            return listener

        return decorator

    def _register(self, event_type: type[E], listener: Callable):
        """
        FOR INTERNAL OR ADVANCED USE ONLY
        Ensures the given event type exists, and registers the listener
        callable within it.

        :param event_type: Type of event being hosted.
        :param listener: Callable that must match event signature.
        """
        event_instance = self.add_event(event_type)
        event_instance._register(listener)

    def add_event(self, event_type: type[E]) -> E:
        """
        Creates a new instance of the event_type given, and adds it to the internal
        event registry, if the event does not already exist.

        :param event_type: The type of the event being added.
        :return: The instance of the event type, either new or extant.
        """
        return self.events.setdefault(event_type, event_type(self))

    def get_event(self, event_type: type[E]) -> E | None:
        """
        Gets the instance of the event type if it exists.

        :param event_type: Type of event to find.
        :return: The event instance if it exists, otherwise None.
        """
        result = self.events.get(event_type, None)
        return cast(E, result)
