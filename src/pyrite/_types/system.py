from __future__ import annotations
from abc import ABC, abstractmethod

import typing

if typing.TYPE_CHECKING:
    from pygame import Event

    from pyrite.events import OnEnable as EventOnEnable
    from pyrite.events import OnDisable as EventOnDisable


class System(ABC):
    """
    Base class for all systems.
    """

    order_index: int
    OnEnable: EventOnEnable
    OnDisable: EventOnDisable

    @property
    @abstractmethod
    def enabled(self) -> bool:
        pass

    @enabled.setter
    @abstractmethod
    def enabled(self, enabled: bool):
        pass

    def pre_update(self) -> None:
        """
        A method that is called during the pre_update phase.
        Will always be called before update.
        """
        pass

    def update(self) -> None:
        """
        A method that is called during the main update phase.
        Most behaviour should happen here.
        """
        pass

    def post_update(self) -> None:
        """
        A method that is called during the post_update phase.
        Will always be called after update.
        """
        pass

    def const_update(self) -> None:
        """
        A method that is called during the const_update phase.
        Useful for behavior that is sensitive to time fluctuations,
        such as physics or AI.

        const_update is called before any other update methods.

        const_update may be called any number of times per frame,
        depending on timestep length.
        """
        pass

    def pre_render(self) -> None:
        """
        A method that is called immediately before the render phase.
        Used by TransformServices to ensure transforms are properly updated just prior
        to being used to display them.
        """

    def on_event(self, event: Event):
        """
        An event hook. Events will be passed to the entity when it's enabled, and can
        be handled here.

        :param event: A pygame event.
        """
        pass
