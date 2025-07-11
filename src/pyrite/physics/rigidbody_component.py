from __future__ import annotations

from typing import Any, TYPE_CHECKING
from weakref import ref

from pymunk import Body

from ..transform import TransformComponent
from ..component import Component
from ..services import PhysicsService

if TYPE_CHECKING:
    from .collider_component import ColliderComponent


class RigidbodyComponent(Component):
    """
    Associates an owner object with a physics body.

    Requires a TransformComponent.

    Required for ColliderComponent and KinematicComponent.

    TODO: Automatically sync Body position with TransformComponent when
    TransformComponent is changed.
    """

    def __init__(self, owner: Any, body: Body | None = None) -> None:
        super().__init__(owner)
        if not (transform := TransformComponent.get(owner)):
            raise RuntimeError(
                f"RigidbodyComponent requires that {owner} has a TransformComponent"
            )
        if body is None:
            body = Body()
        self.transform = transform
        self.body = body
        self._collider: ref[ColliderComponent] | None = None
        PhysicsService.add_rigidbody(self)

    @property
    def collider(self) -> ColliderComponent | None:
        """
        Property tracking an optional ColliderComponent for the Rigidbody

        :return: The owned ColliderComponent, or None
        """
        if self._collider is not None:
            return self._collider()
        return self._collider

    @collider.setter
    def collider(self, collider_component: ColliderComponent | None):
        if collider_component is not None:
            component_reference = ref(collider_component)
        else:
            component_reference = None

        self._collider = component_reference
