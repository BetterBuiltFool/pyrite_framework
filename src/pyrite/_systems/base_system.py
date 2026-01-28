from __future__ import annotations

from typing import TYPE_CHECKING


from pyrite.core.system_manager import SystemManager
from pyrite.core.enableable import Enableable
from pyrite.events import OnEnable, OnDisable
from pyrite._types.system import System

if TYPE_CHECKING:
    pass


class BaseSystem(System, Enableable[SystemManager], manager=SystemManager):
    """
    Base class for all systems that perform actions on components.

    ### Events:
    - OnEnable: Called when the object becomes enabled.
    - OnDisable: Called when the object becomes disabled.
    """

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

    def __init_subclass__(cls, **kwds) -> None:
        return super().__init_subclass__(manager=SystemManager, **kwds)
