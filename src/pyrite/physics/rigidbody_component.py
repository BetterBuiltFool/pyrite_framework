from __future__ import annotations

from typing import Any, TYPE_CHECKING

from pymunk import Body

from ..transform import TransformComponent
from ..types import Component
from .physics_service import PhysicsService

if TYPE_CHECKING:
    pass


class RigidbodyComponent(Component):
    """
    Associates an owner object with a physics body.

    Requires a TransformComponent.

    Required for ColliderComponent and KinematicComponent.

    TODO: Automatically sync Body position with TransformComponent when
    TransformComponent is changed.
    """

    def __init__(self, owner: Any, body: Body = None) -> None:
        super().__init__(owner)
        if not (transform := TransformComponent.get(owner)):
            raise RuntimeError(
                f"RigidbodyComponent requires that {owner} has a TransformComponent"
            )
        if body is None:
            body = Body()
        self.transform = transform
        self.body = body
        PhysicsService.bodies.update({body: owner})
        PhysicsService.space.add(body)
