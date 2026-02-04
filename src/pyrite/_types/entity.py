from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Event

    from pyrite.events import OnDisable as OnDisableEvent, OnEnable as OnEnableEvent


class Entity(Protocol):
    """
    Base class for any class that exhibits behaviour during any of the update phases.
    """

    OnEnable: OnEnableEvent
    OnDisable: OnDisableEvent

    @property
    def enabled(self) -> bool: ...

    @enabled.setter
    def enabled(self, enabled: bool) -> None: ...

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

    def on_event(self, event: Event):
        """
        An event hook. Events will be passed to the entity when it's enabled, and can
        be handled here.

        :param event: A pygame event.
        """
        ...

    def on_preenable(self): ...

    def on_enable(self): ...

    def on_predisable(self): ...

    def on_disable(self): ...
