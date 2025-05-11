from __future__ import annotations

from collections.abc import Sequence
from typing import Any, TYPE_CHECKING

from ..types import Component
from .rigidbody import RigidbodyComponent
from .physics_service import PhysicsService

if TYPE_CHECKING:
    from pymunk import Shape


class ColliderComponent(Component):

    def __init__(self, owner: Any, shape: Shape | Sequence[Shape]) -> None:
        super().__init__(owner)
        if not (rigidbody := RigidbodyComponent.get(owner)):
            raise RuntimeError(
                f"ColliderComponent requires {owner} has a RigidbodyComponent"
            )
        if not isinstance(shape, Sequence):
            shape = [shape]
        self.shapes = shape
        body = rigidbody.body
        for collision_shape in shape:
            collision_shape.body = body
            PhysicsService.space.add(collision_shape)
