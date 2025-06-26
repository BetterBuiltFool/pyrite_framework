from __future__ import annotations

from typing import TYPE_CHECKING

from ..systems import System

from ..services import PhysicsService

if TYPE_CHECKING:
    pass


class PhysicsSystem(System):
    """
    A system that manages the flow of physics in the world space.
    Syncs Rigidbodies and their transforms, and steps the simulation.

    TODO: Pull this out of const_update, give it its own accumulator.
    """

    def __init__(self, physics_mult=1, enabled=True, order_index=0) -> None:
        super().__init__(enabled, order_index)
        self.physics_mult = physics_mult

    def const_update(self, timestep: float) -> None:

        PhysicsService.step(timestep * self.physics_mult)

    def update(self, delta_time: float) -> None:
        PhysicsService.sync_transforms_to_bodies()
