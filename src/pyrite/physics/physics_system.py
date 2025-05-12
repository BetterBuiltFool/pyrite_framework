from __future__ import annotations

import math
from typing import TYPE_CHECKING

from ..types import System
from .physics_service import PhysicsService
from .rigidbody_component import RigidbodyComponent
from ..transform import TransformComponent

if TYPE_CHECKING:
    pass


class PhysicsSystem(System):

    def const_update(self, timestep: float) -> None:

        self.sync_bodies_to_transforms()

        PhysicsService.step(timestep)

        self.sync_transforms_to_bodies()

    def sync_bodies_to_transforms(self):
        """
        Takes all bodies with a TransformComponent and sets their position and rotation
        to match.
        """
        for body, key_object in RigidbodyComponent._bodies.items():
            if not (transform := TransformComponent.get(key_object)):
                continue
            pos = transform.world_position
            body.position = (pos.x, pos.y)
            rot = math.radians(transform.world_rotation)
            body.angle = rot
            PhysicsService.space.reindex_shapes_for_body(body)

    def sync_transforms_to_bodies(self):
        """
        Takes all TransformComponents with a rigidbody and updates their position and
        rotation with the new calculations.
        """
        for body, key_object in RigidbodyComponent._bodies.items():
            if not (transform := TransformComponent.get(key_object)):
                continue
            transform.world_position = body.position
            transform.world_rotation = math.degrees(body.angle)
