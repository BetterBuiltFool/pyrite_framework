from __future__ import annotations

from typing import Any, TYPE_CHECKING

from ..types import System

from .collider_component import ColliderComponent
from ..transform import TransformComponent
from ..services import PhysicsService

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
    """
    A system that manages the flow of physics in the world space.
    Syncs Rigidbodies and their transforms, and steps the simulation.

    TODO: Pull this out of const_update, give it its own accumulator.
    """

    def __init__(self, physics_mult=1, enabled=True, order_index=0) -> None:
        super().__init__(enabled, order_index)
        PhysicsService.set_component_handlers(post_solve=post_solve, separate=separate)
        self.physics_mult = physics_mult

    def const_update(self, timestep: float) -> None:

        PhysicsService.step(timestep * self.physics_mult)

    def update(self, delta_time: float) -> None:
        PhysicsService.sync_transforms_to_bodies(TransformComponent)
