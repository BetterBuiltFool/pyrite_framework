from __future__ import annotations

from typing import Generic, TypeVar

from pyrite.events import OnEnable, OnDisable
from pyrite._types.protocols import Manager

M = TypeVar("M", bound=Manager)


class Enableable(Generic[M]):
    """
    Generic class that allows the subclasses to be handled by a manager class.
    """

    _manager: type[M]

    def __init__(self, enabled=True) -> None:
        self.OnEnable = OnEnable(self)
        self.OnDisable = OnDisable(self)
        self.enabled = enabled

    def __init_subclass__(cls, manager: type[M], **kwds) -> None:
        cls._manager = manager
        super().__init_subclass__(**kwds)

    @property
    def enabled(self) -> bool:
        """
        Whether or not the object is currently active and enabled by the manager.

        Setting this has several hooks that may fire: on_preenable, on_enable,
        on_predisable, on_disable.
        """
        return self._manager.is_enabled(self)

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        self._enabled = enabled
        if enabled:
            self.on_preenable()
            if self._manager.enable(self):
                self.OnEnable(self)
                self.on_enable()
        else:
            self.on_predisable()
            if self._manager.disable(self):
                self.OnDisable(self)
                self.on_disable()

    def on_preenable(self):
        """
        Event called just before the object is enabled.
        Useful if the object needs to be modified before going through the enabling
        process.
        Does NOT guarantee the object is not already enabled.
        """
        pass

    def on_enable(self):
        """
        Event called just after the object has been enabled.
        Useful for when an object needs to perform actions on other objects immediately
        after being enabled.
        Guarantees the object is now enabled, and only runs when the object was
        previously disabled.
        """
        pass

    def on_predisable(self):
        """
        Event called just before the object is disabled.
        Useful if the object needs to perform some kind of cleanup action before
        disabling.
        Does NOT guarantee the object has not already been disabled.
        """
        pass

    def on_disable(self):
        """
        Event called just after the object has been disabled.
        Useful if the object needs to perform and action, like cleanup, only after it
        has been disabled.
        Guarantees the object is now disabled, and that the object was previously
        disabled.
        """
        pass
