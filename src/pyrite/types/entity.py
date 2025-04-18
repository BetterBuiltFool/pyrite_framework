from pyrite.types import Container
from ._base_type import _BaseType

import pygame


class Entity(_BaseType):
    """
    Base class for any class that exhibits behaviour during any of the update phases.
    """

    def __init__(self, container: Container = None, enabled=True) -> None:
        _BaseType.__init__(self, container, enabled)

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

    def on_event(self, event: pygame.Event):
        """
        An event hook. Events will be passed to the entity when it's enabled, and can
        be handled here.

        :param event: A pygame event.
        """
        pass
