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
        self._constraint = pymunk.DampedRotarySpring(
            body_a.body, body_b.body, rest_angle, stiffness, damping
        )
