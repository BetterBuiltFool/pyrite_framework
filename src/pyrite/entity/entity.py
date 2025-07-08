from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import entity_manager
from ..events import OnEnable, OnDisable
from ..types import Entity

if TYPE_CHECKING:
    from pygame import Event


class BaseEntity(Entity):
    """
    Base class for any class that exhibits behaviour during any of the update phases.

    ### Events:
    - OnEnable: Called when the object becomes enabled.
    - OnDisable: Called when the object becomes disabled.
    """

    def __init__(self, enabled=True) -> None:
        self.OnEnable = OnEnable(self)
        self.OnDisable = OnDisable(self)
        self.enabled = enabled

    @property
    def enabled(self) -> bool:
        return entity_manager.is_enabled(self)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        if value:
            self.on_preenable()
            if entity_manager.enable(self):
                self.OnEnable(self)
                self.on_enable()
        else:
            self.on_predisable()
            if entity_manager.disable(self):
                self.OnDisable(self)
                self.on_disable()

    def on_preenable(self):
        pass

    def on_enable(self):
        pass

    def on_predisable(self):
        pass

    def on_disable(self):
        pass

    def pre_update(self, delta_time: float) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def post_update(self, delta_time: float) -> None:
        pass

    def const_update(self, timestep: float) -> None:
        pass

    def on_event(self, event: Event):
        pass
