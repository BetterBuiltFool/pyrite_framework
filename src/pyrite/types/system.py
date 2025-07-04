from __future__ import annotations
from abc import ABC, abstractmethod

import typing

if typing.TYPE_CHECKING:
    from pygame import Event

    from ..events import OnEnable as EventOnEnable


class System(ABC):
    """
    Base class for all systems.
    """

    order_index: int
    OnEnable: EventOnEnable

    @property
    @abstractmethod
    def enabled(self) -> bool:
        pass

    @enabled.setter
    @abstractmethod
    def enabled(self, value: bool):
        pass

    def pre_update(self, delta_time: float) -> None:
        """
        A method that is called during the pre_update phase.
        Will always be called before update.

        :param delta_time: Time passed since last frame.
        """
        pass

    def update(self, delta_time: float) -> None:
        """
        A method that is called during the main update phase.
        Most behaviour should happen here.

        :param delta_time: Time passed since last frame.
        """
        pass

    def post_update(self, delta_time: float) -> None:
        """
        A method that is called during the post_update phase.
        Will always be called after update.

        :param delta_time: Time passed since last frame.
        """
        pass

    def const_update(self, timestep: float) -> None:
        """
        A method that is called during the const_update phase.
        Useful for behavior that is sensitive to time fluctuations,
        such as physics or AI.

        const_update is called before any other update methods.

        const_update may be called any number of times per frame,
        depending on timestep length.

        :param timestep: Length of the timestep being simulated.
        """
        pass

    def pre_render(self, delta_time: float) -> None:
        """
        A method that is called immediately before the render phase.
        Used by TransformServices to ensure transforms are properly updated just prior
        to being used to display them.

        :param delta_time: Time passed since last frame.
        """

    def on_event(self, event: Event):
        """
        An event hook. Events will be passed to the entity when it's enabled, and can
        be handled here.

        :param event: A pygame event.
        """
        pass
