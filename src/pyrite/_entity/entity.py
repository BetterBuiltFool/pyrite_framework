from __future__ import annotations

from typing import TYPE_CHECKING

from pyrite.core.entity_manager import EntityManager
from pyrite.core.enableable import Enableable

if TYPE_CHECKING:
    from pygame import Event


class BaseEntity(Enableable[EntityManager], manager=EntityManager):
    """
    Base class for any class that exhibits behaviour during any of the update phases.

    ### Events:
    - OnEnable: Called when the object becomes enabled.
    - OnDisable: Called when the object becomes disabled.
    """

    def __init_subclass__(cls, **kwds) -> None:
        return super().__init_subclass__(manager=EntityManager, **kwds)

    def pre_update(self) -> None:
        pass

    def update(self) -> None:
        pass

    def post_update(self) -> None:
        pass

    def const_update(self) -> None:
        pass

    def on_event(self, event: Event):
        pass
