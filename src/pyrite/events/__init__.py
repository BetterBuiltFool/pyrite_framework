from typing import TYPE_CHECKING
from ..types.instance_event import InstanceEvent  # noqa:F401

if TYPE_CHECKING:
    from ..collider.collider_component import ColliderComponent

# Define common events here.


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
