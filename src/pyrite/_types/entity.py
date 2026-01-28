from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Event


class Entity(ABC):
    """
    Base class for any class that exhibits behaviour during any of the update phases.
    """

    @abstractmethod
    def pre_update(self) -> None:
        """
        A method that is called during the pre_update phase.
        Will always be called before update.
        """
        ...

    @abstractmethod
    def update(self) -> None:
        """
        A method that is called during the main update phase.
        Most behaviour should happen here.
        """
        ...

    @abstractmethod
    def post_update(self) -> None:
        """
        A method that is called during the post_update phase.
        Will always be called after update.
        """
        ...

    @abstractmethod
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

    @abstractmethod
    def on_event(self, event: Event):
        """
        An event hook. Events will be passed to the entity when it's enabled, and can
        be handled here.

        :param event: A pygame event.
        """
        ...
