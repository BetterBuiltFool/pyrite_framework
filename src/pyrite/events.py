from __future__ import annotations
from typing import TYPE_CHECKING, Any

import pyrite._events.instance_event

if TYPE_CHECKING:
    from pyrite._physics.collider_component import ColliderComponent

# Define common events here.

InstanceEvent = pyrite._events.instance_event.BaseInstanceEvent


class OnTouch(InstanceEvent):
    """
    Called whenever a collider begins contact with another.

    :param this_collider: The collider component belonging to the owner of the instance
        event.
    :param touching: The collider component in contact with _this_collider_
    """

    def __call__(
        self, this_collider: ColliderComponent, touching: ColliderComponent
    ) -> None:
        return super().__call__(this_collider, touching)


class WhileTouching(InstanceEvent):
    """
    Called every frame that two collider components overlap.

    :param this_collider: The collider component belonging to the owner of the instance
        event.
    :param touching: The collider component in contact with _this_collider_
    """

    def __call__(
        self, this_collider: ColliderComponent, touching: ColliderComponent
    ) -> None:
        return super().__call__(this_collider, touching)


class OnSeparate(InstanceEvent):
    """
    Called when a previously touching collider separates.

    :param this_collider: The collider component belonging to the owner of the instance
        event.
    :param touching: The collider component formerly in contact with _this_collider_
    """

    def __call__(
        self, this_collider: ColliderComponent, touching: ColliderComponent
    ) -> None:
        return super().__call__(this_collider, touching)


class OnEnable(InstanceEvent):
    """
    Called when an object move from the disabled state to the enabled state. Does not
    fire if the object is already enabled.

    :param this: The object being enabled.
    """

    def __call__(self, this: Any) -> None:
        return super().__call__(this)


class OnDisable(InstanceEvent):
    """
    Called when an object moves from the enabled state to the disabled state.

    :param this: The object being disnabled.
    """

    def __call__(self, this: Any) -> None:
        return super().__call__(this)
