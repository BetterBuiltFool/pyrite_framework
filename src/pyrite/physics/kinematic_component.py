from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

from pygame import Vector2

from ..component import Component
from .rigidbody_component import RigidbodyComponent

if TYPE_CHECKING:
    from pygame.typing import Point


class KinematicComponent(Component):
    """
    A component that ties into the kinematic attributes of an object's
    RigidbodyComponent.

    Requires RigidbodyComponent.

    TODO: Give methods for manipulating forces on bodies
    """

    def __init__(self, owner: Any) -> None:
        super().__init__(owner)

        if not (rigidbody := RigidbodyComponent.get(owner)):
            raise RuntimeError(
                f"KinematicComponent requires that {owner} has a RigidbodyComponent"
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
    def force(self) -> Vector2:
        """
        Vector2 value of the forces currently acting on the body's venter of gravity.
        """
        return Vector2(self.body.force)

    @property
    def angular_velocity(self) -> float:
        """
        Angular velocity of the object's rigidbody, in degrees/unit time
        """
        return math.degrees(self.body.angular_velocity)

    @angular_velocity.setter
    def angular_velocity(self, ang_velocity: float):
        self.body.angular_velocity = math.radians(ang_velocity)

    @property
    def torque(self) -> float:
        """
        Value representing the torque currently acting on the rigidbody.
        """

        return self.body.torque

    @property
    def rotation_vector(self) -> Vector2:
        """
        Vector2 value of the rotational forces acting on the rigidbody.
        """
        return Vector2(self.body.rotation_vector)

    def apply_force(self, force_vector: Point) -> None:
        self.body.apply_force_at_local_point((force_vector[0], force_vector[1]))

    def apply_impulse(self, impulse_vector: Point) -> None:
        self.body.apply_impulse_at_local_point((impulse_vector[0], impulse_vector[1]))
