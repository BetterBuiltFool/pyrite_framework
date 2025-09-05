from __future__ import annotations

from typing import TYPE_CHECKING
import math

from pygame import Vector2
import pymunk

from pyrite.physics.rigidbody_component import RigidbodyComponent
from ..services import PhysicsService
from ..types.constraint import Constraint
from ..utils import point_to_tuple

if TYPE_CHECKING:
    from pygame.typing import Point


class DampedRotarySpring(Constraint[pymunk.DampedRotarySpring]):
    """
    A damped spring that function with rotation rather than translation.
    """

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        rest_angle: float,
        stiffness: float,
        damping: float,
    ) -> None:
        """
        :param body_a: The primary body of the constraint.
        :param body_b: The secondary body of the  constraint.
        :param rest_angle: The angle which the constraint will tend towards.
        :param stiffness: The spring constant of the constraint (Young's Modulus)
        :param damping: The relative softness of the spring.
        """
        super().__init__(body_a, body_b)

        rest_angle = math.radians(rest_angle)
        self._constraint = pymunk.DampedRotarySpring(
            body_a.body, body_b.body, rest_angle, stiffness, damping
        )

        PhysicsService.add_constraint(self)

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


class DampedSpring(Constraint[pymunk.DampedSpring]):
    """
    A linear spring that configurable softness.
    """

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        anchor_a: Point,
        anchor_b: Point,
        rest_length: float,
        stiffness: float,
        damping: float,
    ) -> None:
        """
        :param body_a: The primary body of the constraint.
        :param body_b: The secondary body of the  constraint.
        :param anchor_a: Relative point on _body_a_ that the spring attaches to.
        :param anchor_b: Relative point on _body_b_ that the spring attaches to.
        :param rest_length: The separation the spring tries to maintain.
        :param stiffness: The spring constant of the constraint (Young's Modulus)
        :param damping: The relative softness of the spring.
        """
        super().__init__(body_a, body_b)

        self._constraint = pymunk.DampedSpring(
            body_a.body,
            body_b.body,
            point_to_tuple(anchor_a),
            point_to_tuple(anchor_b),
            rest_length,
            stiffness,
            damping,
        )

        PhysicsService.add_constraint(self)

    @property
    def anchor_a(self) -> Vector2:
        """
        Relative position of the contraint on body A.
        """
        return Vector2(self._constraint.anchor_a)

    @anchor_a.setter
    def anchor_a(self, anchor_a: Point) -> None:
        self._constraint.anchor_a = point_to_tuple(anchor_a)

    @property
    def anchor_b(self) -> Vector2:
        """
        Relative position of the contraint on body B.
        """
        return Vector2(self._constraint.anchor_b)

    @anchor_b.setter
    def anchor_b(self, anchor_b: Point) -> None:
        self._constraint.anchor_b = point_to_tuple(anchor_b)

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
    def rest_length(self) -> float:
        """
        The length the spring tries to return to.
        """
        return self._constraint.rest_length

    @rest_length.setter
    def rest_length(self, rest_length: float) -> None:
        self._constraint.rest_length = rest_length

    @property
    def stiffness(self) -> float:
        """
        The spring constant of the joint.
        """
        return self._constraint.stiffness

    @stiffness.setter
    def stiffness(self, stiffness: float) -> None:
        self._constraint.stiffness = stiffness


class GearJoint(Constraint[pymunk.GearJoint]):
    """
    A Rotary joint that maintain a constant ratio of angle between two rigidbodies.
    """

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        phase: float,
        ratio: float,
    ) -> None:
        """
        :param body_a: The primary body of the constraint.
        :param body_b: The secondary body of the  constraint.
        :param phase: The offset angle between the two bodies, in degrees.
        :param ratio: Absolute ratio between the two bodies constrained by the gear
            joint.
        """
        super().__init__(body_a, body_b)

        self._constraint = pymunk.GearJoint(
            body_a.body, body_b.body, phase, ratio
        )  # TODO: math.radians(phase)

        PhysicsService.add_constraint(self)

    @property
    def phase(self) -> float:
        """
        The offset angle between the two bodies, in degrees.
        """
        return math.degrees(self._constraint.phase)

    @phase.setter
    def phase(self, phase: float) -> None:
        self._constraint.phase = math.radians(phase)

    @property
    def ratio(self) -> float:
        """
        Absolute ratio between the two bodies constrained by the gear joint.
        """
        return self._constraint.ratio

    @ratio.setter
    def ratio(self, ratio: float) -> None:
        self._constraint.ratio = ratio


class GrooveJoint(Constraint[pymunk.GrooveJoint]):
    """
    A pivot joint that can also slide.
    """

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        groove_a: Point,
        groove_b: Point,
        anchor_b: Point,
    ) -> None:
        """
        :param body_a: The primary body of the constraint.
        :param body_b: The secondary body of the  constraint.
        :param groove_a: Position of the start of the groove.
        :param groove_b: Position of the end of the groove.
        :param anchor_b: Pivot point on _body_b_.
        """
        super().__init__(body_a, body_b)

        self._constraint = pymunk.GrooveJoint(
            body_a.body,
            body_b.body,
            point_to_tuple(groove_a),
            point_to_tuple(groove_b),
            point_to_tuple(anchor_b),
        )

        PhysicsService.add_constraint(self)

    @property
    def anchor_b(self) -> Vector2:
        """
        Pivot point on body B.
        """
        return Vector2(self._constraint.anchor_b)

    @anchor_b.setter
    def anchor_b(self, anchor_b: Point) -> None:
        self._constraint.anchor_b = point_to_tuple(anchor_b)

    @property
    def groove_a(self) -> Vector2:
        """
        Position of the start of the groove.
        """
        return Vector2(self._constraint.groove_a)

    @groove_a.setter
    def groove_a(self, groove_a: Point) -> None:
        self._constraint.groove_a = point_to_tuple(groove_a)

    @property
    def groove_b(self) -> Vector2:
        """
        Position of the end of the groove.
        """
        return Vector2(self._constraint.groove_b)

    @groove_b.setter
    def groove_b(self, groove_b: Point) -> None:
        self._constraint.groove_b = point_to_tuple(groove_b)


class PinJoint(Constraint[pymunk.PinJoint]):
    """
    Simple rigid joint that holds two rigidbodies together.
    """

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        anchor_a: Point = (0, 0),
        anchor_b: Point = (0, 0),
    ) -> None:
        """
        :param body_a: The primary body of the constraint.
        :param body_b: The secondary body of the  constraint.
        :param anchor_a: Relative point on _body_a_ that the spring attaches to.
        :param anchor_b: Relative point on _body_b_ that the spring attaches to.
        """
        super().__init__(body_a, body_b)

        self._constraint = pymunk.PinJoint(
            body_a.body,
            body_b.body,
            point_to_tuple(anchor_a),
            point_to_tuple(anchor_b),
        )

        PhysicsService.add_constraint(self)

    @property
    def anchor_a(self) -> Vector2:
        """
        Relative position of the contraint on body A.
        """
        return Vector2(self._constraint.anchor_a)

    @anchor_a.setter
    def anchor_a(self, anchor_a: Point) -> None:
        self._constraint.anchor_a = point_to_tuple(anchor_a)

    @property
    def anchor_b(self) -> Vector2:
        """
        Relative position of the contraint on body B.
        """
        return Vector2(self._constraint.anchor_b)

    @anchor_b.setter
    def anchor_b(self, anchor_b: Point) -> None:
        self._constraint.anchor_b = point_to_tuple(anchor_b)


class PivotJoint(Constraint[pymunk.PivotJoint]):
    """
    A pin-like joint that also allows for rotation of body B relative to body A.

    Do not spawn PivotJoints directly. Instead, use `PivotJoint.from_pivot()` or
    `PivotJoint.from_anchors()`
    """

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        _constraint: pymunk.PivotJoint,
    ) -> None:
        """
        Do not spawn PivotJoints directly. Instead, use `PivotJoint.from_pivot()` or
        `PivotJoint.from_anchors()`
        """
        super().__init__(body_a, body_b)

        self._constraint = _constraint

        PhysicsService.add_constraint(self)

    @staticmethod
    def from_pivot(
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        pivot: Point,
    ) -> PivotJoint:
        """
        Creates a PivotJoint between two bodies, around a world-space point.

        Make sure the rigidbodies are in the correct space already.

        :param body_a: The first Rigidbody of the joint
        :param body_b: The second Rigidbody of the joint
        :param pivot: A world-space position around which body_b will pivot
        :return: The completed PivotJoint
        """
        _constraint = pymunk.PivotJoint(body_a.body, body_b.body, point_to_tuple(pivot))
        return PivotJoint(body_a, body_b, _constraint)

    @staticmethod
    def from_anchors(
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        anchor_a: Point,
        anchor_b: Point,
    ) -> PivotJoint:
        """
        Creates a PivotJoint between two Rigidbodies, with anchor points relative to
        each body.

        Make sure the rigidbodies are in the correct space already.

        :param body_a: The first Rigidbody of the joint
        :param body_b: The second Rigidbody of the joint
        :param anchor_a: A local position on _body_a_
        :param anchor_b: A local position on _body_b_
        :return: The completed PivotJoint
        """
        _constraint = pymunk.PivotJoint(
            body_a.body, body_b.body, point_to_tuple(anchor_a), point_to_tuple(anchor_b)
        )
        return PivotJoint(body_a, body_b, _constraint)

    @property
    def anchor_a(self) -> Vector2:
        """
        Relative position of the contraint on body A.
        """
        return Vector2(self._constraint.anchor_a)

    @anchor_a.setter
    def anchor_a(self, anchor_a: Point) -> None:
        self._constraint.anchor_a = point_to_tuple(anchor_a)

    @property
    def anchor_b(self) -> Vector2:
        """
        Relative position of the contraint on body B.
        """
        return Vector2(self._constraint.anchor_b)

    @anchor_b.setter
    def anchor_b(self, anchor_b: Point) -> None:
        self._constraint.anchor_b = point_to_tuple(anchor_b)


class RatchetJoint(Constraint[pymunk.RatchetJoint]):
    """
    A pivoting joint that works like a socket wrench.
    """

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        phase: float,
        ratchet: float,
    ) -> None:
        """
        :param body_a: The primary body of the constraint.
        :param body_b: The secondary body of the  constraint.
        :param phase: The offset angle between the two bodies, in degrees.
        :param ratchet: The size of the step in the ratchet mechanism.
        """
        super().__init__(body_a, body_b)

        self._constraint = pymunk.RatchetJoint(
            body_a.body, body_b.body, phase, ratchet
        )  # TODO: math.radians(phase)

        PhysicsService.add_constraint(self)

    @property
    def angle(self) -> float:
        """
        The current angle of the joint, in degrees.
        """
        return math.degrees(self._constraint.angle)

    @angle.setter
    def angle(self, angle: float) -> None:
        self._constraint.angle = math.radians(angle)

    @property
    def phase(self) -> float:
        """
        The offset angle between the two bodies, in degrees.
        """
        return math.degrees(self._constraint.phase)

    @phase.setter
    def phase(self, phase: float) -> None:
        self._constraint.phase = math.radians(phase)

    @property
    def ratchet(self) -> float:
        """
        The size of the step in the ratchet mechanism.
        """
        return self._constraint.ratchet

    @ratchet.setter
    def reatchet(self, ratchet: float) -> None:
        self._constraint.ratchet = ratchet


class RotaryLimitJoint(Constraint[pymunk.RotaryLimitJoint]):
    """
    A pivoting joint with a maximum and minimum angle.
    """

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        min: float,
        max: float,
    ) -> None:
        """
        :param body_a: The primary body of the constraint.
        :param body_b: The secondary body of the  constraint.
        :param min: The lower bound of the rotation range, in degrees.
        :param max: The upper bound of the rotation range, in degrees.
        """
        super().__init__(body_a, body_b)

        self._constraint = pymunk.RotaryLimitJoint(
            body_a.body, body_b.body, math.radians(min), math.radians(max)
        )

        PhysicsService.add_constraint(self)

    @property
    def min(self) -> float:
        """
        The lower bound of the rotation range, in degrees.
        """
        return math.degrees(self._constraint.min)

    @min.setter
    def min(self, min: float) -> None:
        self._constraint.min = math.radians(min)

    @property
    def max(self) -> float:
        """
        The upper bound of the rotation range, in degrees.
        """
        return math.degrees(self._constraint.max)

    @max.setter
    def max(self, max: float) -> None:
        self._constraint.max = math.radians(max)


class SimpleMotor(Constraint[pymunk.SimpleMotor]):
    """
    A rotating joint that maintains a constant angular velocity.
    """

    def __init__(
        self, body_a: RigidbodyComponent, body_b: RigidbodyComponent, rate: float
    ) -> None:
        """
        :param body_a: The primary body of the constraint.
        :param body_b: The secondary body of the  constraint.
        :param rate: Relative angular velocity.
        """
        super().__init__(body_a, body_b)

        self._constraint = pymunk.SimpleMotor(
            body_a.body, body_b.body, math.radians(rate)
        )

        PhysicsService.add_constraint(self)

    @property
    def rate(self) -> float:
        """
        Relative angular velocity.
        """
        return math.degrees(self._constraint.rate)

    @rate.setter
    def rate(self, rate: float) -> None:
        self._constraint.rate = math.radians(rate)


class SlideJoint(Constraint[pymunk.SlideJoint]):
    """
    A pin-like joint that allows for limited movement between the constrained
    rigidbodies.
    """

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        anchor_a: Point,
        anchor_b: Point,
        min: float,
        max: float,
    ) -> None:
        """
        :param body_a: The first Rigidbody of the joint
        :param body_b: The second Rigidbody of the joint
        :param anchor_a: A local position on _body_a_
        :param anchor_b: A local position on _body_b_
        :param min: The lower bound of the distance between anchor points.
        :param max: The upper bound of the distance between anchor points.
        """
        super().__init__(body_a, body_b)

        self._constraint = pymunk.SlideJoint(
            body_a.body,
            body_b.body,
            point_to_tuple(anchor_a),
            point_to_tuple(anchor_b),
            min,
            max,
        )

        PhysicsService.add_constraint(self)

    @property
    def anchor_a(self) -> Vector2:
        """
        Relative position of the contraint on body A.
        """
        return Vector2(self._constraint.anchor_a)

    @anchor_a.setter
    def anchor_a(self, anchor_a: Point) -> None:
        self._constraint.anchor_a = point_to_tuple(anchor_a)

    @property
    def anchor_b(self) -> Vector2:
        """
        Relative position of the contraint on body B.
        """
        return Vector2(self._constraint.anchor_b)

    @anchor_b.setter
    def anchor_b(self, anchor_b: Point) -> None:
        self._constraint.anchor_b = point_to_tuple(anchor_b)

    @property
    def min(self) -> float:
        """
        The lower bound of the distance between anchor points.
        """
        return math.degrees(self._constraint.min)

    @min.setter
    def min(self, min: float) -> None:
        self._constraint.min = math.radians(min)

    @property
    def max(self) -> float:
        """
        The upper bound of the distance between anchor points.
        """
        return math.degrees(self._constraint.max)

    @max.setter
    def max(self, max: float) -> None:
        self._constraint.max = math.radians(max)
