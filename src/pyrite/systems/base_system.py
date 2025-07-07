from __future__ import annotations

from typing import TYPE_CHECKING


from ..core import system_manager
from ..events import OnEnable, OnDisable
from ..types import System

if TYPE_CHECKING:
    pass


class BaseSystem(System):

    def __init__(self, enabled: bool = True, order_index: int = 0) -> None:
        """
        Base class for all systems.

        :param enabled: Whether the system should be running at instantiation,
            defaults to True
        :param order_index: Relative order in which the system should be run, with
            priority going down as value increases, but negative numbers are
            approximately distance from last, defaults to 0 (Tie for first)
        """
        self.OnEnable = OnEnable(self)
        self.OnDisable = OnDisable(self)
        self._enabled = None
        self.enabled = enabled
        self.order_index = order_index

    @property
    def enabled(self) -> bool:
        return system_manager.is_enabled(self)

    @enabled.setter
    def enabled(self, value: bool):
        if value:
            system_manager.enable(self)
            if not self._enabled:
                self.OnEnable(self)
        else:
            system_manager.disable(self)
            if self._enabled:
                self.OnDisable(self)
        self._enabled = value
