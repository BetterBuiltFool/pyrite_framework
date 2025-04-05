from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar

from weakref import WeakValueDictionary

if TYPE_CHECKING:
    from ..types.system import System
    from pygame import Event


SystemType = TypeVar("SystemType", bound=System)


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
    def get_system(self, system_type: type[SystemType]) -> SystemType:
        """
        Returns the instance that matches the system type.

        :param system_type: The system type whose instance we are searching for.
        :return: The instance of the system type
        :raises: KeyError if no such instance exists.
        """
        pass

    @abstractmethod
    def remove_system(self, system_type: type[SystemType]) -> SystemType:
        """
        Removes a system instance from all parts of the system manager,
        based on the system type.

        :param system_type: The system type whose instance is to be removed.
        :return: The system instance that was removed.
        :raises: KeyError if no such instance exists.
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


class DefaultSystemManager(SystemManager):

    def __init__(self) -> None:
        self.systems: WeakValueDictionary[type[System], System] = WeakValueDictionary()
