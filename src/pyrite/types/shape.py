from __future__ import annotations

from typing import TYPE_CHECKING

import pymunk

from pygame import Rect, Vector2

from ..utils import point_to_tuple

if TYPE_CHECKING:
    from pygame.typing import Point

    from weakref import ref
    from ..physics import ColliderComponent, RigidbodyComponent


class Shape[ShapeT: pymunk.Shape]:

    def __init__(self) -> None:
        self._rigidbody: RigidbodyComponent | None
        self._collider: ref[ColliderComponent] | None
        self._shape: ShapeT

    @property
    def area(self) -> float:
        return self._shape.area

    @property
    def bounding_box(self) -> Rect:
        bb = self._shape.bb
        left, top, right, bottom = bb.left, bb.top, bb.right, bb.bottom
        width = right - left
        height = top - bottom
        return Rect(left, top, width, height)

    @property
    def collider(self) -> ColliderComponent | None:
        """
        The ColliderComponent the shape is attached to. If None, the shape is not
        attached to any rigidbody.

        :return: A ColliderComponent, or None if unattached.
        """
        if self._collider:
            return self._collider()
        return None

    @collider.setter
    def collider(self, collider: ColliderComponent | None) -> None:
        if self.collider is not None:
            # del self.collider.shapes[self]
            pass
        if collider is None:
            self._collider = None
            return
        self._collider = ref(collider)
        # collider.shapes[self] = None

    @property
    def center_of_gravity(self) -> Vector2:
        """
        Returns the calculated center of gravity for this shape.
        """
        return Vector2(self._shape.center_of_gravity)

    @property
    def density(self) -> float:
        """
        Density of the shape.

        Useful for allowing the mass and inertia of a rigidbody to be calculated
        automatically from the sum of its shapes rather than being set to the body.
        """
        return self._shape.density

    @density.setter
    def density(self, density: float) -> None:
        self._shape.density = density

    @property
    def elasticity(self) -> float:
        """
        Elasticity of the shape.

        0.0 is perfectly inelastic, while 1.0 is perfectly elastic, causing a "perfect"
        bounce. Values greater than or equal to 1.0 can cause issues in the simulation.
        """
        return self._shape.elasticity

    @elasticity.setter
    def elasticity(self, elasticity: float) -> None:
        self._shape.elasticity = elasticity

    # Leaving out 'filter' property, since we set that inside ColliderComponent

    @property
    def friction(self) -> float:
        """
        Coefficient of friction of the shape. 0.0 is frictionless, number greater than
        1.0 are okay.
        """
        return self._shape.friction

    @friction.setter
    def friction(self, friction: float) -> None:
        self._shape.friction = friction

    @property
    def mass(self) -> float:
        """
        The mass of the shape.
        """
        return self._shape.mass

    @mass.setter
    def mass(self, mass: float) -> None:
        self._shape.mass = mass

    @property
    def moment(self) -> float:
        """
        The calculated moment of inertia of the shape.
        """
        return self._shape.moment

    @property
    def sensor(self) -> bool:
        """
        Boolean if the shape is a sensor. Sensor generate collision events, but do not
        cause actual collisions.
        """
        return self._shape.sensor

    @sensor.setter
    def sensor(self, sensor: bool) -> None:
        self._shape.sensor = sensor

    @property
    def surface_velocity(self) -> Vector2:
        """
        Velocity applied to other shapes in contact with this shape.
        """
        return Vector2(self._shape.surface_velocity)

    @surface_velocity.setter
    def surface_velocity(self, surface_velocity: Point) -> None:
        self._shape.surface_velocity = point_to_tuple(surface_velocity)
