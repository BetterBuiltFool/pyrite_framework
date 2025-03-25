from __future__ import annotations

from abc import ABC
from collections.abc import Callable
from typing import TypeVar
from weakref import ref, WeakKeyDictionary


T = TypeVar("T", bound="EventBase")
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
        # EventBase instance is still around. We don't need to keep hold on the
        # EventBase instance.
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


class EventBase(ABC):
    def __init__(self) -> None:
        self.events: dict[type[InstanceEvent], InstanceEvent] = {}

    def add_listener(self, event: type[InstanceEvent]) -> Callable:

        def decorator(listener: Callable) -> Callable:
            self._register(event, listener)
            return listener

        return decorator

    def _register(self, event: type[E], listener: Callable):
        pass

    def add_event(self, event: type[E]) -> E:
        pass

    def get_event(self, event_type: type[E]) -> E | None:
        pass
