from __future__ import annotations
from abc import ABC

import typing

from ..core import system_manager as sm

if typing.TYPE_CHECKING:
    from ..core.system_manager import SystemManager
    from pygame import Event


class System(ABC):

    def __init__(
        self, enabled=True, order_index=0, system_manager: SystemManager = None
    ) -> None:
        """
        Base class for all systems.

        :param enabled: Whether the system should be running at instantiation,
            defaults to True
        :param order_index: Relative order in which the system should be run, with
            priority going down as value increases, but negative numbers are
            approximately distance from last, defaults to 0 (Tie for first)
        """
        if system_manager is None:
            system_manager = sm.get_system_manager()
        self.system_manager = system_manager
        self._enabled = None
        self.enabled = enabled
        self.order_index = order_index

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        if value:
            self.system_manager.enable(self)
        else:
            self.system_manager.disable(self)

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

    def pre_render(self, delta_time: float) -> None:
        """
        A method that is called immediately before the render phase.
        Used by TransformServices to ensure transforms are properly updated just prior
        to being used to display them.

        :param delta_time: Time passed since last frame.
        """

    def on_event(self, event: Event):
        """
        An event hook. Events will be passed to the entity when it's enabled, and can
        be handled here.

        :param event: A pygame event.
        """
        pass
