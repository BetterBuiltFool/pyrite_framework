from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.system import System
    from pygame import Event


class SystemManager(ABC):

    @abstractmethod
    def enable(self, system: System) -> bool:
        """
        Adds a system to the collection of active systems.

        :param item: System being enabled.
        :return: True if enable is successful, False if not, such as system already
        enabled.
        """
        pass

    @abstractmethod
    def disable(self, system: System) -> bool:
        """
        Removes a system from the collection of active systems.

        :param item: System being enabled.
        :return: True if disable is successful, False if not, such as system already
        disabled.
        """
        pass

    @abstractmethod
    def pre_update(self, delta_time: float):
        """
        Runs the pre_update phase for active systems.

        :param delta_time: Time passed since last frame
        """
        pass

    @abstractmethod
    def update(self, delta_time: float):
        """
        Runs the update phase for active systems.

        :param delta_time: Time passed since last frame
        """
        pass

    @abstractmethod
    def post_update(self, delta_time: float):
        """
        Runs the post_update phase for active systems.

        :param delta_time: Time passed since last frame
        """
        pass

    @abstractmethod
    def const_update(self, timestep: float):
        """
        Runs the const_update phase for active systems.

        :param timestep: Length of the simulated step
        """
        pass

    @abstractmethod
    def handle_event(self, event: Event):
        """
        Passes the event down to all active systems.

        :param event: A pygame event.
        """
        pass
