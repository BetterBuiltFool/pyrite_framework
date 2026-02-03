from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Event

    from pyrite.events import OnEnable as OnEnableEvent, OnDisable as OnDisableEvent


class System(Protocol):
    """
    Base class for all systems.
    """

    OnEnable: OnEnableEvent
    OnDisable: OnDisableEvent
    order_index: int

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

    @property
    def enabled(self) -> bool: ...

    @enabled.setter
    def enabled(self, enabled: bool) -> None: ...

    def on_preenable(self): ...

    def on_enable(self): ...

    def on_predisable(self): ...

    def on_disable(self): ...
