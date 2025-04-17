from __future__ import annotations

from abc import ABC, abstractmethod
import bisect
from typing import TYPE_CHECKING, TypeVar
from weakref import WeakSet


if TYPE_CHECKING:
    from collections.abc import Sequence
    from ..types.system import System
    from pygame import Event


SystemType = TypeVar("SystemType")


_active_system_manager: SystemManager = None


def get_system_manager() -> SystemManager:
    return _active_system_manager


def set_system_manager(manager: SystemManager):
    global _active_system_manager
    _active_system_manager = manager


_deferred_enables: set[System] = set()


def enable(system: System):
    if _active_system_manager:
        _active_system_manager.enable(system)
        return
    _deferred_enables.add(system)


def disable(system: System):
    if _active_system_manager:
        _active_system_manager.disable(system)
        return
    _deferred_enables.discard(system)


class SystemManager(ABC):

    def __init__(self) -> None:
        # Subclasses must call super().__init__ at the END of initialization
        for system in _deferred_enables:
            self.enable(system)

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
    def get_system(self, system_type: type[SystemType]) -> SystemType | None:
        """
        Returns the instance that matches the system type.

        :param system_type: The system type whose instance we are searching for.
        :return: The instance of the system type, if it exists, else None
        """
        pass

    @abstractmethod
    def remove_system(self, system_type: type[SystemType]) -> SystemType:
        """
        Removes a system instance from all parts of the system manager,
        based on the system type.

        :param system_type: The system type whose instance is to be removed.
        :return: The system instance that was removed.
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
    def pre_render(self, delta_time: float):
        """
        Runs the pre_render phase for active systems.

        :param delta_time: Time passed since last frame
        """

    @abstractmethod
    def handle_event(self, event: Event):
        """
        Passes the event down to all active systems.

        :param event: A pygame event.
        """
        pass

    def prepare_systems(self):
        """
        Signals to the system manager that a frame is beginning, and to do whatever it
        needs to in order to prepare for the new frame.
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
        self.systems: dict[type[System], System] = {}
        self.active_systems: WeakSet[System] = WeakSet()
        self.current_systems: list[System] = []
        super().__init__()

    def enable(self, system: System) -> bool:
        self._capture_system(system)
        if system not in self.active_systems:
            self.active_systems.add(system)
            return True
        return False

    def disable(self, system: System) -> bool:
        if system in self.active_systems:
            self.active_systems.remove(system)
            return True
        return False

    def _capture_system(self, system: System):
        if system.__class__ not in self.systems:  # I don't this is needed?
            self.systems.update({system.__class__: system})

    def get_system(self, system_type: type[SystemType]) -> SystemType | None:
        return self.systems.get(system_type)

    def remove_system(self, system_type: type[SystemType]) -> SystemType:
        system = self.systems.pop(system_type)
        self.active_systems.discard(system)
        return system

    def prepare_systems(self):
        self.current_systems = self.sort_systems(self.active_systems)

    def pre_update(self, delta_time: float):
        for system in self.current_systems:
            system.pre_update(delta_time)

    def update(self, delta_time: float):
        for system in self.current_systems:
            system.update(delta_time)

    def post_update(self, delta_time: float):
        for system in self.current_systems:
            system.post_update(delta_time)

    def const_update(self, timestep: float):
        for system in self.current_systems:
            system.const_update(timestep)

    def pre_render(self, delta_time: float):
        for system in self.current_systems:
            system.pre_render(delta_time)

    def handle_event(self, event: Event):
        for system in self.current_systems:
            system.on_event(event)

    def sort_systems(self, systems: Sequence[System]) -> list[System]:
        """
        Converts the incoming sequence to a sorted list, where the order goes as
        follows:

        0 --> Infinity, -Infinity --> -1

        :param systems: A sequence of systems, to be sorted
        :return: A sorted list of the same systems
        """
        systems = sorted(systems, key=_get_system_index)
        pivot = bisect.bisect_left(systems, 0, key=_get_system_index)
        negatives = systems[:pivot]
        del systems[:pivot]

        negatives.reverse()

        return systems + negatives


def _get_system_index(system: System) -> int:
    return system.order_index


_default_system_manager_type = DefaultSystemManager


def get_default_system_manager_type() -> type[SystemManager]:
    return _default_system_manager_type


def set_default_system_manager_type(manager_type: type[SystemManager]):
    global _default_system_manager_type
    _default_system_manager_type = manager_type
