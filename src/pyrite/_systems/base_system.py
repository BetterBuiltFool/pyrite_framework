from __future__ import annotations

from typing import TYPE_CHECKING


from pyrite.core.system_manager import SystemManager
from pyrite.core.enableable import Enableable

# from pyrite.events import OnEnable, OnDisable
# from pyrite._types.system import System

if TYPE_CHECKING:
    from pygame import Event


class BaseSystem(Enableable[SystemManager], manager=SystemManager):
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
        super().__init__(enabled)
        # self.OnEnable = OnEnable(self)
        # self.OnDisable = OnDisable(self)
        # self._enabled = None
        # self.enabled = enabled
        self.order_index = order_index

    def __init_subclass__(cls, **kwds) -> None:
        return super().__init_subclass__(manager=SystemManager, **kwds)

    def pre_update(self) -> None:
        """
        A method that is called during the pre_update phase.
        Will always be called before update.
        """
        ...

    def update(self) -> None:
        """
        A method that is called during the main update phase.
        Most behaviour should happen here.
        """
        ...

    def post_update(self) -> None:
        """
        A method that is called during the post_update phase.
        Will always be called after update.
        """
        ...

    def const_update(self) -> None:
        """
        A method that is called during the const_update phase.
        Useful for behavior that is sensitive to time fluctuations,
        such as physics or AI.

        const_update is called before any other update methods.

        const_update may be called any number of times per frame,
        depending on timestep length.
        """
        ...

    def pre_render(self) -> None:
        """
        A method that is called immediately before the render phase.
        Used by TransformServices to ensure transforms are properly updated just prior
        to being used to display them.
        """
        ...

    def on_event(self, event: Event):
        """
        An event hook. Events will be passed to the entity when it's enabled, and can
        be handled here.

        :param event: A pygame event.
        """
        ...
