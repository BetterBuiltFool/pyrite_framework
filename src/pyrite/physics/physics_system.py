from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pymunk

from ..types import System
from .. import physics
from .physics_service import PhysicsService
from ..transform import TransformComponent, transform_service

if TYPE_CHECKING:
    pass


class PhysicsSystem(System):

    def const_update(self, timestep: float) -> None:

        self.sync_bodies_to_transforms()

        PhysicsService.step(timestep)

        self.sync_transforms_to_bodies()

    def update(self, delta_time: float) -> None:
        self.sync_transforms_to_bodies()

    def sync_bodies_to_transforms(self):
        """
        Takes all bodies with a TransformComponent and sets their position and rotation
        to match.
        """
        for body, key_object in physics._bodies.items():
            if not (transform := TransformComponent.get(key_object)):
                continue
            vel = body.velocity
            ang_vel = body.angular_velocity
            pos = transform.world_position
            body.position = (pos.x, pos.y)
            rot = math.radians(transform.world_rotation)
            body.angle = rot
            body.velocity = vel
            body.angular_velocity = ang_vel
            PhysicsService.space.reindex_shapes_for_body(body)

    def sync_transforms_to_bodies(self):
        """
        Takes all TransformComponents with a rigidbody and updates their position and
        rotation with the new calculations.
        """
        for body, key_object in physics._bodies.items():
            if (
                not (transform := TransformComponent.get(key_object))
                or body.is_sleeping
                or body.body_type == pymunk.Body.STATIC
            ):
                # No adjustments to sleeping, static, or transformless objects
                continue
            new_pos = transform.world_position.lerp(body.position, 0.1)
            angle_between = (
                (math.degrees(body.angle) - transform.world_rotation) + 180
            ) % 360 - 180
            new_rot = angle_between / 2

            # print(f"{key_object} {new_pos=}, {transform.world_position=}")

            transform_service.set_world_position(transform, new_pos)
            transform_service.set_world_rotation(transform, new_rot)

            # transform.world_position = body.position
            # transform.world_rotation = math.degrees(body.angle)
