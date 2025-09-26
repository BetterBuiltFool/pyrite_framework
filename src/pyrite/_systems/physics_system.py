from __future__ import annotations

from typing import TYPE_CHECKING

from pyrite._systems.base_system import BaseSystem

from pyrite._services.physics_service import PhysicsServiceProvider as PhysicsService
from pyrite._services.transform_service import (
    TransformServiceProvider as TransformService,
)


if TYPE_CHECKING:
    pass


class PhysicsSystem(BaseSystem):
    """
    A system that manages the flow of physics in the world space.
    Syncs Rigidbodies and their transforms, and steps the simulation.

    TODO: Pull this out of const_update, give it its own accumulator.
    """

    def __init__(self, physics_mult=1, enabled=True, order_index=0) -> None:
        super().__init__(enabled, order_index)
        self.physics_mult = physics_mult

    def const_update(self, timestep: float) -> None:
        # Ensure that the rigidbodies are where we want them to be.
        # If multiple constupdates are happening, this might cause issues.
        # TODO: Move this elsewhere so that it only happens once per frame?
        PhysicsService.sync_bodies_to_transforms()

        PhysicsService.step(timestep * self.physics_mult)

    def update(self, delta_time: float) -> None:
        self.sync_transforms_to_bodies()

    def sync_transforms_to_bodies(self):
        for rigidbody, transform in PhysicsService.get_updated_transforms_for_bodies():
            transform_component = rigidbody.transform
            TransformService._set_world_no_update(transform_component, transform)
