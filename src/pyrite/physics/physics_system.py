from __future__ import annotations

import math
from typing import Any, TYPE_CHECKING

import pymunk

from ..types import System
from .physics_service import PhysicsService
from .collider_component import ColliderComponent
from ..transform import TransformComponent, transform_service

if TYPE_CHECKING:
    from pymunk import (
        Arbiter,
        Space,
    )


# Figure out where to put this so it doesn't cause circular imports
# Track _bodies here? Would remove RigidbodyComponent import
def post_solve(arbiter: Arbiter, space: Space, data: Any):
    collider1, collider2 = get_collider_components(arbiter)
    if arbiter.is_first_contact:
        if collider1.compare_mask(collider2):
            collider1.OnTouch(collider1, collider2)
        if collider2.compare_mask(collider1):
            collider2.OnTouch(collider2, collider1)
    if collider1.compare_mask(collider2):
        collider1.WhileTouching(collider1, collider2)
    if collider2.compare_mask(collider1):
        collider2.WhileTouching(collider2, collider1)


def separate(arbiter: Arbiter, space: Space, data: Any):
    collider1, collider2 = get_collider_components(arbiter)
    if collider1.compare_mask(collider2):
        collider1.OnSeparate(collider1, collider2)
    if collider2.compare_mask(collider1):
        collider2.OnSeparate(collider2, collider1)


def get_collider_components(
    arbiter: Arbiter,
) -> tuple[ColliderComponent, ColliderComponent]:
    shape1, shape2 = arbiter.shapes
    body1 = shape1.body
    body2 = shape2.body
    owner1 = PhysicsService.get_owner_from_body(body1)
    owner2 = PhysicsService.get_owner_from_body(body2)
    return ColliderComponent.get(owner1), ColliderComponent.get(owner2)


class PhysicsSystem(System):

    def __init__(self, physics_mult=1, enabled=True, order_index=0) -> None:
        super().__init__(enabled, order_index)
        PhysicsService.comp_handler.post_solve = post_solve
        PhysicsService.comp_handler.separate = separate
        self.physics_mult = physics_mult

    def const_update(self, timestep: float) -> None:

        self.sync_bodies_to_transforms()

        PhysicsService.step(timestep * self.physics_mult)

    def update(self, delta_time: float) -> None:
        self.sync_transforms_to_bodies()

    def sync_bodies_to_transforms(self):
        """
        Takes all bodies with a TransformComponent and sets their position and rotation
        to match.
        """
        for body, key_object in PhysicsService.bodies.items():
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
        for body, key_object in PhysicsService.bodies.items():
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
