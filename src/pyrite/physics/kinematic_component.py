from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

from pygame import Vector2

from ..types import Component
from .rigidbody_component import RigidbodyComponent

if TYPE_CHECKING:
    from pygame.typing import Point


class KinematicComponent(Component):
    """
    A component that ties into the kinematic attributes of an object's
    RigidbodyComponent.

    Requires RigidbodyComponent.
    """

    def __init__(self, owner: Any) -> None:
        super().__init__(owner)

        if not (rigidbody := RigidbodyComponent.get(owner)):
            raise RuntimeError(
                f"ColliderComponent requires that {owner} has a RigidbodyComponent"
            )
        self.body = rigidbody.body

    @property
    def velocity(self) -> Vector2:
        """
        Vector2 velocity of the object's rigidbody
        """
        vel = self.body.velocity
        return Vector2(vel[0], vel[1])

    @velocity.setter
    def velocity(self, vel: Point):
        self.body.velocity = (vel[0], vel[1])

    @property
    def angular_velocity(self) -> float:
        """
        Angular velocity of the object's rigidbody, in degrees/unit time
        """
        return math.degrees(self.body.angular_velocity)

    @angular_velocity.setter
    def angular_velocity(self, ang_velocity: float):
        self.body.angular_velocity = math.radians(ang_velocity)
