from __future__ import annotations

from typing import TYPE_CHECKING
import math

from pygame import Vector2
import pymunk

from pyrite.physics.rigidbody_component import RigidbodyComponent

from ..types.constraint import Constraint

if TYPE_CHECKING:
    from pygame.typing import Point


def point_to_tuple(point: Point) -> tuple[float, float]:
    return point[0], point[1]


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


class DampedSpring(Constraint[pymunk.DampedSpring]):

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

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        phase: float,
        ratio: float,
    ) -> None:
        super().__init__(body_a, body_b)

        self._constraint = pymunk.GearJoint(body_a.body, body_b.body, phase, ratio)

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

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        groove_a: Point,
        groove_b: Point,
        anchor_b: Point,
    ) -> None:
        super().__init__(body_a, body_b)

        self._constraint = pymunk.GrooveJoint(
            body_a.body,
            body_b.body,
            point_to_tuple(groove_a),
            point_to_tuple(groove_b),
            point_to_tuple(anchor_b),
        )

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

    def __init__(
        self,
        body_a: RigidbodyComponent,
        body_b: RigidbodyComponent,
        anchor_a: Point = (0, 0),
        anchor_b: Point = (0, 0),
    ) -> None:
        super().__init__(body_a, body_b)

        self._constraint = pymunk.PinJoint(
            body_a.body,
            body_b.body,
            point_to_tuple(anchor_a),
            point_to_tuple(anchor_b),
        )

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
