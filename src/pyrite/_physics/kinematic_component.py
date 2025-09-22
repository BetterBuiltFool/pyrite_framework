from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

from pygame import Vector2

from pyrite._component.component import BaseComponent as Component
from pyrite._physics.rigidbody_component import RigidbodyComponent
from pyrite.utils import point_to_tuple

if TYPE_CHECKING:
    from pygame.typing import Point


class KinematicComponent(Component):
    """
    A component that ties into the kinematic attributes of an object's
    RigidbodyComponent.

    Requires RigidbodyComponent.

    :raises RuntimeError: Raised if the owner does not have a RigidbodyComponent.
    """

    def __init__(self, owner: Any) -> None:
        super().__init__(owner)

        if not (rigidbody := RigidbodyComponent.get(owner)):
            raise RuntimeError(
                f"KinematicComponent requires that {owner} has a RigidbodyComponent"
            )
        self.body = rigidbody.body

    @property
    def angular_velocity(self) -> float:
        """
        Angular velocity of the object's rigidbody, in degrees/unit time
        """
        return math.degrees(self.body.angular_velocity)

    @angular_velocity.setter
    def angular_velocity(self, angular_velocity: float):
        self.body.angular_velocity = math.radians(angular_velocity)

    @property
    def force(self) -> Vector2:
        """
        Vector2 value of the forces currently acting on the body's venter of gravity.
        """
        return Vector2(self.body.force)

    @property
    def kinetic_energy(self) -> float:
        """
        The current kinetic energy of the Rigidbody.
        """
        return self.body.kinetic_energy

    @property
    def rotation_vector(self) -> Vector2:
        """
        Vector2 value of the rotational forces acting on the rigidbody.
        """
        return Vector2(self.body.rotation_vector)

    @property
    def torque(self) -> float:
        """
        Value representing the torque currently acting on the rigidbody.
        """

        return self.body.torque

    @property
    def velocity(self) -> Vector2:
        """
        Vector2 velocity of the object's rigidbody
        """
        return Vector2(self.body.velocity)

    @velocity.setter
    def velocity(self, velocity: Point):
        self.body.velocity = point_to_tuple(velocity)

    def apply_force(self, force_vector: Point) -> None:
        """
        Applies the given force to the center of the Rigidbody.

        :param force_vector: A 2D force vector, with local rotation.
        """
        self.body.apply_force_at_local_point(point_to_tuple(force_vector))

    def apply_impulse(self, impulse_vector: Point) -> None:
        """
        Applies the given impulse to the center of the Rigidbody.

        :param force_vector: A 2D impulse vector, with local rotation.
        """
        self.body.apply_impulse_at_local_point(point_to_tuple(impulse_vector))
