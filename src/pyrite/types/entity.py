from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import entity_manager
from .._helper import defaults

if TYPE_CHECKING:
    from . import Container

import pygame


class Entity:
    """
    Base class for any class that exhibits behaviour during any of the update phases.
    """

    def __init__(self, container: Container = None, enabled=True) -> None:
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
        if self.container is None:
            return
        if value:
            self.on_preenable()
            if entity_manager.enable(self):
                self.on_enable()
        else:
            self.on_predisable()
            if entity_manager.disable(self):
                self.on_disable()

    def on_preenable(self):
        """
        Event called just before the object is enabled.
        Useful if the object needs to be modified before going through the enabling
        process.
        Does NOT guarantee the object is not already enabled.

        """
        print(f"Enabling {self=}")

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

    def pre_update(self, delta_time: float) -> None:
        """
        A method that is called during the pre_update phase.
        Will always be called before update.

        :param delta_time: Time passed since last frame.
        """
        pass

    def update(self, delta_time: float) -> None:
        """
        A method that is called during the main update phase.
        Most behaviour should happen here.

        :param delta_time: Time passed since last frame.
        """
        pass

    def post_update(self, delta_time: float) -> None:
        """
        A method that is called during the post_update phase.
        Will always be called after update.

        :param delta_time: Time passed since last frame.
        """
        pass

    def const_update(self, timestep: float) -> None:
        """
        A method that is called during the const_update phase.
        Useful for behavior that is sensitive to time fluctuations,
        such as physics or AI.

        const_update is called before any other update methods.

        const_update may be called any number of times per frame,
        depending on timestep length.

        :param timestep: Length of the timestep being simulated.
        """
        pass

    def on_event(self, event: pygame.Event):
        """
        An event hook. Events will be passed to the entity when it's enabled, and can
        be handled here.

        :param event: A pygame event.
        """
        pass
