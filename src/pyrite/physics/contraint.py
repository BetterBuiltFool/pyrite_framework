from __future__ import annotations

from typing import TYPE_CHECKING

import math

import pymunk

from pyrite.physics.rigidbody_component import RigidbodyComponent

from ..types.constraint import Constraint

if TYPE_CHECKING:
    pass


class DampedRotarySpring(Constraint[pymunk.DampedRotarySpring]):

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        rest_angle: float,
        stiffness: float,
        damping: float,
    ) -> None:
        super().__init__(body_a, body_b)

        rest_angle = math.radians(rest_angle)
        self._constraint = pymunk.DampedRotarySpring(
            body_a.body, body_b.body, rest_angle, stiffness, damping
        )

    @property
    def damping(self) -> float:
        """
        Controls the apparent "softness" of the spring.
        Higher values result in stiffer springs.
        """
        return self._constraint.damping

    @damping.setter
    def damping(self, damping: float) -> None:
        self._constraint.damping = damping

    @property
    def rest_angle(self) -> float:
        """
        The angle the spring will try to return to, in degrees.
        """
        return math.degrees(self._constraint.rest_angle)

    @rest_angle.setter
    def rest_angle(self, rest_angle: float) -> None:
        self._constraint.rest_angle = math.radians(rest_angle)

    @property
    def stiffness(self) -> float:
        """
        The spring constant of the joint.
        """
        return self._constraint.stiffness

    @stiffness.setter
    def stiffness(self, stiffness: float) -> None:
        self._constraint.stiffness = stiffness
