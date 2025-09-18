from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from functools import singledispatchmethod
from typing import Any, TYPE_CHECKING
from weakref import ref, WeakKeyDictionary

from pyrite._types.instance_event import InstanceEvent

# This is NOT the standard library threading module.
from ..utils import threading

if TYPE_CHECKING:
    pass


class _Sentinel:

    pass


SENTINEL = _Sentinel()


class BaseInstanceEvent[T](InstanceEvent):
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
        self.listeners: WeakKeyDictionary[Any, list[Callable]] = WeakKeyDictionary()
        """
        A set containing all listeners for this event instance.

        TODO: Consider who should be responsible for tracking listeners.
        Currently, the object creating the listener is responsible, with this set only
        being for calling them.
        """

    @property
    def instance(self) -> T | None:
        # Provides dereferenced access to the owning instance
        return self._instance()

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> None:
        self._notify(*args, **kwds)

    @singledispatchmethod
    def add_listener(self, arg) -> Callable:
        raise NotImplementedError("Argument type not supported")

    @add_listener.register(Callable)  # type: ignore
    def _(self, listener: Callable) -> Callable:
        self._register(SENTINEL, listener)
        return listener

    @add_listener.register(object)
    def _(self, caller: object) -> Callable:

        def inner(listener: Callable):
            self._register(caller, listener)
            return listener

        return inner

    def _register(self, caller, listener: Callable):
        listeners = self.listeners.setdefault(caller, [])
        # TODO Test if method, keep methods and function in two different sets?
        listeners.append(listener)

    def _deregister(self, listener: Callable):
        for caller, listeners in self.listeners.items():
            if listener in listeners:
                listeners.remove(listener)
                # Note: if a listener managed to get in there multiple times,
                # this will only remove one occurence.
                # If that happens, though, something went horribly wrong.
                # See you in 2 years!
                break

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
        # rule. Add a separate list and registration method for those.
        for caller, listeners in self.listeners.items():
            # The pyrite threading module can be set to run regular threads or asyncio
            # threads.
            if caller is not SENTINEL:
                for listener in listeners:
                    threading.start_thread(listener, *(caller, *args))
                continue
            for listener in listeners:
                threading.start_thread(listener, *args)
