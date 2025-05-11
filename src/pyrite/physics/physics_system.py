from __future__ import annotations

from typing import TYPE_CHECKING

from ..types import System
from .physics_service import PhysicsService

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
        pass

    def sync_transforms_to_bodies(self):
        """
        Takes all TransformComponents with a rigidbody and updates their position and
        rotation with the new calculations.
        """
        pass
