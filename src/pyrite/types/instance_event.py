from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TypeVar
from weakref import proxy, ref, WeakSet, ProxyTypes

# This is NOT the standard library threading module.
from ..utils import threading


T = TypeVar("T")
E = TypeVar("E", bound="InstanceEvent")


def weaken_closures(listener: Callable) -> Callable:
    """
    Converts a callable's closures to proxies, so the callable doesn't prevent garbage
    collection on the enclosed objects.

    Makes no changes if the callable has no closures, or if the closures are already
    proxied.

    :return: The listener, without strong references.
    """
    if listener.__closure__ is None:
        return listener

    for cell in listener.__closure__:
        contents = cell.cell_contents
        # Instance checks are relatively slow, but we're only doing this occasionally.
        # ...
        # You are only doing this occasionally, right?
        if isinstance(contents, ProxyTypes):
            continue
        cell.cell_contents = proxy(contents)

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

    The attributes should have docstrings containing the event signature of the event
    they relate to.

    Instance event classes should start with "On" to convey that they are events.
    """

    def __init__(self, instance: T) -> None:
        """
        Creates a new instance of the Instance Event.

        :param instance: The object the instance event is tied to. This allows access
        to the owning instance if needed.
        """
        self._instance = ref(instance)
        self.listeners: WeakSet[Callable] = WeakSet()
        """
        A set containing all listeners for this event instance.

        TODO: Consider who should be responsible for tracking listeners.
        Currently, the object creating the listener is responsible, with this set only
        being for calling them.
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

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> None:
        self._notify(*args, **kwds)

    def add_listener(self, listener: Callable) -> Callable:
        """
        Adds a function, method, or other callable to this InstanceEvent's listeners.
        That listener will be called whenever the event is fired.

        Listeners will be called in threads. If the game is being run is Async mode,
        all listeners must be coroutines, even without sleep statements.
        TODO: Make this automatic somehow?

        To use within a class, an inner function can be used as the listener, usually
        best to set this up in the initializer, or any method that is only called once.
        You will also need to maintain a reference to each listener inside the instance
        to prevent it from being garbage collected.

        Example:
        ____________________________________________________________________________________________

        class A:

            def __init__(self):
                self.event_haver = SomeEntity()

                @self.event_haver.OnSomeEvent.add_listener
                def listener_name(event_param1, event_param2):
                    print(self)
                    # Do something

                self.event_listeners = [listener_name]
        ____________________________________________________________________________________________

        Every instance of A will create its own listener, which can reference "self" to
        refer to that instance, while also allowing access to the event's
        parameters.

        Note: This method will remove strong references in any closures in the listener.
        This means the listener function will not prevent the creating object from
        being garbage collected.

        :return: The original listener, to be available for reuse and access.
        """
        self._register(weaken_closures(listener))
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
