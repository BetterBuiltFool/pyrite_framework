from __future__ import annotations
from typing import TYPE_CHECKING, Any

from hair_trigger import Event


if TYPE_CHECKING:
    from pyrite._component.collider_component import ColliderComponent

# Define common events here.


class OnTouch(Event):
    """
    Called whenever a collider begins contact with another.

    :param this_collider: The collider component belonging to the owner of the instance
        event.
    :param touching: The collider component in contact with _this_collider_
    """

    def trigger(
        self, this_collider: ColliderComponent, touching: ColliderComponent
    ) -> None:
        return super().trigger(this_collider, touching)


class WhileTouching(Event):
    """
    Called every frame that two collider components overlap.

    :param this_collider: The collider component belonging to the owner of the instance
        event.
    :param touching: The collider component in contact with _this_collider_
    """

    def trigger(
        self, this_collider: ColliderComponent, touching: ColliderComponent
    ) -> None:
        return super().trigger(this_collider, touching)


class OnSeparate(Event):
    """
    Called when a previously touching collider separates.

    :param this_collider: The collider component belonging to the owner of the instance
        event.
    :param touching: The collider component formerly in contact with _this_collider_
    """

    def trigger(
        self, this_collider: ColliderComponent, touching: ColliderComponent
    ) -> None:
        return super().trigger(this_collider, touching)


class OnEnable(Event):
    """
    Called when an object move from the disabled state to the enabled state. Does not
    fire if the object is already enabled.

    :param this: The object being enabled.
    """

    def trigger(self, this: Any) -> None:
        return super().trigger(this)


class OnDisable(Event):
    """
    Called when an object moves from the enabled state to the disabled state.

    :param this: The object being disnabled.
    """

    def trigger(self, this: Any) -> None:
        return super().trigger(this)
