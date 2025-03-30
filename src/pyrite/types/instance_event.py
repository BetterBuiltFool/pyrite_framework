from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TypeVar
from weakref import proxy, ref, WeakKeyDictionary, WeakSet

# This is NOT the standard library threading module.
from ..utils import threading


T = TypeVar("T")
E = TypeVar("E", bound="InstanceEvent")


def weaken_closures(listener: Callable) -> Callable:
    """
    Converts a callable's closures to proxies, so the callable doesn't prevent garbage
    collection on the enclosed objects.

    Makes no changes if the callable has no closures.

    :return: The listener, without strong references.
    """
    if listener.__closure__ is None:
        return listener

    for cell in listener.__closure__:
        cell.cell_contents = proxy(cell.cell_contents)

    return listener


class InstanceEvent(ABC):
    """
    Events that are bound to an instance of an object. They accumulate listeners, which
    respond when the event fires.

    The __call__ method defines the event's parameters, which will be passed on to the
    listener. The listener must be able to receive these parameters, or else will error.
    For implementation of __call__, either forward the event parameters to
    super().__call__() [The default], or forward them into _notify().

    For user-created events, they are fired by calling the event, passing along its
    parameters.

    ------------------Naming Conventions-----------------

    Objects with instance events should have those events as attributes. Pyrite uses
    PascalCase/UpperCamelCase for event attribute names, like used with class names, to
    help to convey that they are a distinct type of attribute.

    Instance event classes should start with "On" to convey that they are events.
    """

    instances: WeakKeyDictionary[T, InstanceEvent] = WeakKeyDictionary()

    def __init__(self, instance: T) -> None:
        """
        Creates a new instance of the Instance Event.

        :param instance: The object the instance event is tied to. This allows access
        to the owning instance if needed.
        """
        self._instance = ref(instance)
        self.listeners = WeakSet()
        """
        A set containing all listeners for this event instance.
        TODO Find a way to eliminate the listener after its parent is dead.
        Otherwise, will hold up GC
        Solution: Use WeakKeyDictionary w/ the listener owner as the key
        Change add_listener to descriptor?
        """

    @property
    def instance(self) -> T | None:
        """
        The owning instance of the event.

        Weakly stored to so garbage collection can happen normally, but this property
        allows direct access to the instance as long as it still exists.
        """
        # Provides dereferenced access to the owning instance
        return self._instance()

    def __init_subclass__(cls) -> None:
        # Using a WeakKeyDictionary since we only need the instance if the
        # HasEvents instance is still around. We don't need to keep hold on the
        # HasEvents instance.
        cls.instances = WeakKeyDictionary()

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> None:
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
