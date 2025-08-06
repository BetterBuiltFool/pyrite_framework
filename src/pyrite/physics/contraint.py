from __future__ import annotations

from typing import TYPE_CHECKING

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
        # TODO Convert rest_angle to radians. We want to be user-facing values to be in
        # degrees to match other places.
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
