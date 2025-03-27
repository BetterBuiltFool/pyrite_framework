from __future__ import annotations

from abc import ABC
from collections.abc import Callable
from typing import Any, TypeVar
from weakref import ref, WeakKeyDictionary

# This is NOT the standard library threading module.
from ..utils import threading


T = TypeVar("T")
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
        """

    def __init_subclass__(cls) -> None:
        # Using a WeakKeyDictionary since we only need the instance if the
        # HasEvents instance is still around. We don't need to keep hold on the
        # HasEvents instance.
        cls.instances = WeakKeyDictionary()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self._notify(*args, **kwds)

    def add_listener(self, listener: Callable) -> Callable:
        """
        Adds a function, method, or other callable to this InstanceEvent's listeners.
        That listener will be called whenever the event is fired.

        Listeners will be called in threads. If the game is being run is Async mode,
        all listeners must be coroutines, even without sleep statements.

        To use within a class, an inner function can be used as the listener, usually
        best to set this up in the initializer.

        Example:
        ____________________________________________________________________________________________

        class A:

            def __init__(self):
                self.event_haver = SomeEntity()

                @self.event_haver.OnSomeEvent.add_listener
                def _(event_param1, event_param2):
                    print(self)
                    # Do something
        ____________________________________________________________________________________________

        Every instance of A will create its own listener, which can reference "self" to
        refer to that instance, while also allowing access to the event's
        parameters.

        :return: The original listener, to be available for reuse.
        """
        self._register(listener)
        return listener

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
        """

        # Decision was made for all instance event listeners to be async.
        # The risk of race conditions is inevitable, and while synchronous calls can't
        # technically form race conditions, the fact that they can be called at any
        # time means it's always possible to have even a sync event make a change at an
        # unexpected time, mirorring a race condition.

        # Threads also adds the benefit of an exception not necessarily crashing the
        # entire game, just the thread.

        # TODO If there is demand for sync listeners, make them the exception, not the
        # rule. Add a seperate list and registration method for those.
        for listener in self.listeners:
            # The pyrite threading module can be set to run regular threads or asyncio
            # threads.
            threading.start_thread(listener, *args)
            # listener(*args, **kwds)
