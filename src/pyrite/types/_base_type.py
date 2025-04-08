from __future__ import annotations

from typing import TYPE_CHECKING

from .._helper import defaults

from .. import game

if TYPE_CHECKING:
    from . import Container
    from . import System


class _BaseType:

    def __init__(self, container: Container = None, enabled=True) -> None:
        # super().__init__()
        if container is None:
            container = defaults.get_default_container()
        self.container: Container = container
        self.enabled = enabled

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        # if self.container is None:
        if self.container is None:
            return
        if value:
            self.on_preenable()
            if self.container.enable(self):
                self.on_enable()
        else:
            self.on_predisable()
            if self.container.disable(self):
                self.on_disable()

    def add_to_system(self, system_type: type[System]):
        if system := self.get_system(system_type):
            system.register(self)

    def remove_from_system(self, system_type: type[System]):
        if system := self.get_system(system_type):
            system.deregister(self)

    def get_system(self, system_type: type[System]) -> System | None:
        system_manager = game.get_system_manager()
        return system_manager.get_system(system_type)

    def on_preenable(self):
        """
        Event called just before the object is enabled.
        Useful if the object needs to be modified before going through the enabling
        process.
        Does NOT guarantee the object is not already enabled.

        """

    def on_enable(self):
        """
        Event called just after the object has been enabled.
        Useful for when an object needs to perform actions on other objects immediately
        after being enabled.
        Guarantees the object is now enabled, and only runs when the object was
        previously disabled.
        """

    def on_predisable(self):
        """
        Event called just before the object is disabled.
        Useful if the object needs to perform some kind of cleanup action before
        disabling.
        Does NOT guarantee the object has not already been disabled.
        """

    def on_disable(self):
        """
        Event called just after the object has been disabled.
        Useful if the object needs to perform and action, like cleanup, only after it
        has been disabled.
        Guarantees the object is now disabled, and that the object was previously
        disabled.
        """
