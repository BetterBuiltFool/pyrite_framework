from __future__ import annotations

from abc import ABC, abstractmethod
import bisect
from typing import cast, Self, TYPE_CHECKING
from weakref import WeakSet

from pyrite._types.system import System

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pygame import Event


_deferred_enables: set[System] = set()


class SystemManager:
    _active_system_manager: AbstractSystemManager

    @classmethod
    def enable(cls, item: System) -> bool:
        """
        Adds a system to the collection of active systems.

        :param item: System being enabled.
        :return: True if enable is successful, False if not, such as system already
        enabled.
        """
        # Only runs when a proper system manager doesn't exist yet
        flag = item not in _deferred_enables
        _deferred_enables.add(item)
        return flag

    @classmethod
    def _enable_wrapper(cls, item: System) -> bool:
        return cls._active_system_manager.enable(item)

    @classmethod
    def disable(cls, item: System) -> bool:
        """
        Removes a system from the collection of active systems.

        :param item: System being enabled.
        :return: True if disable is successful, False if not, such as system already
        disabled.
        """
        # Only runs when a proper system manager doesn't exist yet
        flag = item in _deferred_enables
        _deferred_enables.discard(item)
        return flag

    @classmethod
    def _disable_wrapper(cls, item: System) -> bool:
        """
        Determines if the passed system is currently considered enabled by the manager.

        :param item: Any system
        :return: True if currently enabled, False if disabled
        """
        return cls._active_system_manager.disable(item)

    @classmethod
    def is_enabled(cls, item: System) -> bool:
        """
        Determines if the passed system is currently considered enabled by the manager.

        :param system: Any system
        :return: True if currently enabled, False if disabled
        """
        return False

    @classmethod
    def _is_enabled_wrapper(cls, item: System) -> bool:
        return cls._active_system_manager.is_enabled(item)

    @classmethod
    def _activate(cls) -> None:
        """
        Changes the methods to run their wrapper versions instead of the deferred
        versions.
        """
        cls.enable = cls._enable_wrapper
        cls.disable = cls._disable_wrapper
        cls.is_enabled = cls._is_enabled_wrapper

    @classmethod
    def set_system_manager(cls, manager: AbstractSystemManager) -> None:
        cls._active_system_manager = manager
        cls._activate()

    @staticmethod
    def get_system_manager(**kwds) -> AbstractSystemManager:
        if (system_manager := kwds.get("system_manager", None)) is None:
            manager_type = get_default_system_manager_type()
            system_manager = manager_type()
        return system_manager


class AbstractSystemManager(ABC):

    def __new__(cls) -> Self:
        new_manager = super().__new__(cls)
        SystemManager.set_system_manager(new_manager)
        return new_manager

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
    def is_enabled(self, system: System) -> bool:
        """
        Determines if the passed system is currently considered enabled by the manager.

        :param system: Any system
        :return: True if currently enabled, False if disabled
        """
        pass

    @abstractmethod
    def get_system[SystemType: System](
        self, system_type: type[SystemType]
    ) -> SystemType | None:
        """
        Returns the instance that matches the system type.

        :param system_type: The system type whose instance we are searching for.
        :return: The instance of the system type, if it exists, else None
        """
        pass

    @abstractmethod
    def remove_system[SystemType: System](
        self, system_type: type[SystemType]
    ) -> SystemType:
        """
        Removes a system instance from all parts of the system manager,
        based on the system type.

        :param system_type: The system type whose instance is to be removed.
        :return: The system instance that was removed.
        """
        pass

    @abstractmethod
    def pre_update(self):
        """
        Runs the pre_update phase for active systems.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Runs the update phase for active systems.
        """
        pass

    @abstractmethod
    def post_update(self):
        """
        Runs the post_update phase for active systems.
        """
        pass

    @abstractmethod
    def const_update(self):
        """
        Runs the const_update phase for active systems.
        """
        pass

    @abstractmethod
    def pre_render(self):
        """
        Runs the pre_render phase for active systems.
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


class DefaultSystemManager(AbstractSystemManager):

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

    def is_enabled(self, system: System) -> bool:
        return system in self.active_systems

    def _capture_system(self, system: System):
        if system.__class__ not in self.systems:  # I don't this is needed?
            self.systems[system.__class__] = system

    def get_system[SystemType: System](
        self, system_type: type[SystemType]
    ) -> SystemType | None:
        system = self.systems.get(system_type)
        if system is not None:
            system = cast(SystemType, system)
        return system

    def remove_system[SystemType: System](
        self, system_type: type[SystemType]
    ) -> SystemType:
        system = self.systems.pop(system_type)
        self.active_systems.discard(system)
        if system is not None:
            system = cast(SystemType, system)
        return system

    def prepare_systems(self):
        self.current_systems = self.sort_systems(self.active_systems)

    def pre_update(self):
        for system in self.current_systems:
            system.pre_update()

    def update(self):
        for system in self.current_systems:
            system.update()

    def post_update(self):
        for system in self.current_systems:
            system.post_update()

    def const_update(self):
        for system in self.current_systems:
            system.const_update()

    def pre_render(self):
        for system in self.current_systems:
            system.pre_render()

    def handle_event(self, event: Event):
        for system in self.current_systems:
            system.on_event(event)

    def sort_systems(self, systems: Iterable[System]) -> list[System]:
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


def get_default_system_manager_type() -> type[AbstractSystemManager]:
    return _default_system_manager_type


def set_default_system_manager_type(manager_type: type[AbstractSystemManager]):
    global _default_system_manager_type
    _default_system_manager_type = manager_type
