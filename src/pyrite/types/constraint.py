from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pymunk import Constraint as PymunkConstraint
    from ..physics.rigidbody_component import RigidbodyComponent


class Constraint[ConstraintT: PymunkConstraint]:
    """
    ABC class for physics contraints. All constraints are adapters for the underlying
    physics engine.
    """

    def __init__(self, body_a: RigidbodyComponent, body_b: RigidbodyComponent) -> None:
        self._a = body_a
        self._b = body_b
        self._constraint: ConstraintT

    @property
    def a(self) -> RigidbodyComponent:
        """
        The first of the two constrained rigidbodies.
        """
        return self._a

    @property
    def b(self) -> RigidbodyComponent:
        """
        The second of the two constrained rigidbodies.
        """
        return self._b

    @property
    def collide_bodies(self) -> bool:
        """
        When False,on any constraint that ties together two bodies, the bodies will
        ignore collisions with each other.

        Defaults to True.
        """
        return self._constraint.collide_bodies

    @collide_bodies.setter
    def collide_bodies(self, collide_bodies: bool) -> None:
        self._constraint.collide_bodies = collide_bodies

    @property
    def error_bias(self) -> float:
        """
        The percentage of joint error that remains unfixed after one second.

        Defaults to pow(1.0 - 0.1, 60.0), or 10% correction every 1/60 second.
        """
        return self._constraint.error_bias

    @error_bias.setter
    def error_bias(self, error_bias: float) -> None:
        self._constraint.error_bias = error_bias

    @property
    def impulse(self) -> float:
        """
        The most recent impulse this constraint applied.

        Multiply by the physics step to determine force.
        """
        return self._constraint.impulse

    @property
    def max_bias(self) -> float:
        """
        The maximum speed that the constraint will apply error correction.

        Defaults to infinity.
        """
        return self._constraint.max_bias

    @max_bias.setter
    def max_bias(self, max_bias: float) -> None:
        self._constraint.max_bias = max_bias

    @property
    def max_force(self) -> float:
        """
        The maximum force the constraint can apply to its two bodies.

        Defaults to fnfinity.
        """
        return self._constraint.max_force

    @max_force.setter
    def max_force(self, max_force: float) -> None:
        self._constraint.max_force = max_force

    # Not adding post/presolve right now.

    def activate_bodies(self) -> None:
        """
        Activates the constrained bodies.
        """
        self._constraint.activate_bodies()
