from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar
from weakref import WeakSet, WeakValueDictionary

from ..types.system import System

if TYPE_CHECKING:
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

    @staticmethod
    def get_system_manager(**kwds) -> SystemManager:
        if (system_manager := kwds.get("system_manager", None)) is None:
            manager_type = get_default_system_manager_type()
            system_manager = manager_type()
        return system_manager


class DefaultSystemManager(SystemManager):

    def __init__(self) -> None:
        self.systems: WeakValueDictionary[type[SystemType], SystemType] = (
            WeakValueDictionary()
        )
        self.active_systems: WeakSet[SystemType] = WeakSet()

    def enable(self, system: System) -> bool:
        self._capture_system(system)
        if system not in self.active_systems:
            self.active_systems.add(system)
            return True
        return False

    def disable(self, system: System) -> bool:
        self._capture_system(system)
        if system in self.active_systems:
            self.active_systems.remove(system)
            return True
        return False

    def _capture_system(self, system: System):
        if system.__class__ not in self.systems:
            self.systems.update({system.__class__, system})

    def get_system(self, system_type: type[SystemType]) -> SystemType:
        system = self.systems.get(system_type)
        if not system:
            raise KeyError(f"Cannot get system {system_type}, it is not being managed.")

    def remove_system(self, system_type: type[SystemType]) -> SystemType:
        system = self.systems.pop(system_type)
        if not system:
            raise KeyError(
                f"Cannot remove system {system_type}, it is not being managed."
            )
        self.active_systems.discard(system)
        return system

    def pre_update(self, delta_time: float):
        for system in self.active_systems:
            system.pre_update(delta_time)

    def update(self, delta_time: float):
        for system in self.active_systems:
            system.update(delta_time)

    def post_update(self, delta_time: float):
        for system in self.active_systems:
            system.post_update(delta_time)

    def const_update(self, timestep: float):
        for system in self.active_systems:
            system.const_update(timestep)

    def handle_event(self, event: Event):
        for system in self.active_systems:
            system.on_event(event)


_default_system_manager_type = DefaultSystemManager


def get_default_system_manager_type() -> type[SystemManager]:
    return _default_system_manager_type


def set_default_system_manager_type(manager_type: type[SystemManager]):
    global _default_system_manager_type
    _default_system_manager_type = manager_type
