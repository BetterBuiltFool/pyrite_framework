from __future__ import annotations

import math
from typing import TYPE_CHECKING
import unittest

from pyrite.constants import MASK_ALL
from pyrite.physics import ColliderComponent, RigidbodyComponent
from pyrite._physics.shapes import Circle
from pyrite._physics.filter import Filter
from pyrite._services.physics_service import PhysicsServiceProvider as PhysicsService
from pyrite._services.physics_service import PymunkPhysicsService
from pyrite.transform import TransformComponent, Transform

if TYPE_CHECKING:
    from pygame.typing import Point
    from pyrite._physics.queries import SegmentInfo
    from pyrite._types.shape import Shape


FILTER = Filter(0, MASK_ALL, MASK_ALL)


class Empty:

    def __init__(self) -> None:
        self.transform = TransformComponent(self)
        self.rigidbody = RigidbodyComponent(self)


class TestPymunkPhysicsService(unittest.TestCase):

    def assertInRay(
        self, collider: ColliderComponent, ray_query_infos: list[SegmentInfo]
    ):
        for segment_info in ray_query_infos:
            for shape in collider.shapes:
                if shape is segment_info.shape:
                    return True
        raise AssertionError(f"{collider} is not found in the ray query")

    def setUp(self) -> None:
        self.physics_service = PymunkPhysicsService()

        # This ensures we're working with a clean service for each test.

        PhysicsService.hotswap(self.physics_service)

    def test_remove_collider_shape(self):
        collider_owner = Empty()

        test_shape = Circle(None, 10)
        test_shape_2 = Circle(None, 15)
        collider = ColliderComponent(collider_owner, [test_shape, test_shape_2])

        self.assertIn(test_shape, collider.shapes)
        self.assertIn(test_shape_2, collider.shapes)

        self.physics_service.remove_collider_shape(collider, test_shape)

        self.assertNotIn(test_shape, collider.shapes)
        self.assertIn(test_shape_2, collider.shapes)

    def test_clear_collider_shapes(self):
        collider_owner = Empty()

        test_shape = Circle(None, 10)
        test_shape_2 = Circle(None, 15)
        collider = ColliderComponent(collider_owner, [test_shape, test_shape_2])

        self.assertIn(test_shape, collider.shapes)
        self.assertIn(test_shape_2, collider.shapes)

        self.physics_service.clear_collider_shapes(collider)

        self.assertNotIn(test_shape, collider.shapes)
        self.assertNotIn(test_shape_2, collider.shapes)

    def test_force_sync_to_transform(self):
        phys_object = Empty()

        phys_object.rigidbody.body.position = (10, 10)
        phys_object.rigidbody.body.angle = math.radians(45)

        transform = Transform((100, 100), 90)
        phys_object.transform.world_position = transform.position
        phys_object.transform.world_rotation = transform.rotation

        self.assertNotEqual(
            phys_object.transform.world_position, phys_object.rigidbody.body.position
        )
        self.assertNotEqual(
            phys_object.transform.world_rotation,
            math.degrees(phys_object.rigidbody.body.angle),
        )

        self.physics_service._force_sync_to_transform(phys_object.rigidbody)

        self.assertEqual(
            phys_object.transform.world_position, phys_object.rigidbody.body.position
        )
        self.assertEqual(
            phys_object.transform.world_rotation,
            math.degrees(phys_object.rigidbody.body.angle),
        )

    def test_get_updated_transforms(self):
        phys_object = Empty()

        phys_object.rigidbody.body.position = (0, 0)
        phys_object.rigidbody.body.angle = math.radians(0)

        transform = Transform((100, 100), 90)
        phys_object.transform.world_position = transform.position
        phys_object.transform.world_rotation = transform.rotation

        expected = Transform((50, 50), 45)

        for _, transform in self.physics_service.get_updated_transforms_for_bodies():
            self.assertEqual(transform.position, expected.position)
            self.assertEqual(transform.rotation, expected.rotation)

    def test_cast_ray_single(self) -> None:
        ball1 = Empty()
        circle1 = Circle(None, 10)
        ColliderComponent(ball1, circle1)

        ball2 = Empty()
        circle2 = Circle(None, 10)
        ColliderComponent(ball2, circle2)
        ball2.rigidbody.transform.position = (-20, 0)

        self.physics_service._force_sync_to_transform(ball2.rigidbody)

        params_list: list[tuple[Point, Point, float, Shape | None]] = [
            ((0, 0), (-20, 0), 0, circle1),
            ((20, 0), (40, 0), 0, None),
            ((-20, 0), (0, 0), 0, circle2),
        ]

        for i, (start, end, radius, expected) in enumerate(params_list):
            with self.subTest(i=i):
                query = self.physics_service.cast_ray_single(start, end, radius, FILTER)
                target = None
                if query:
                    target = query.shape
                self.assertIs(target, expected)

    def test_cast_ray(self) -> None:
        ball1 = Empty()
        circle1 = Circle(None, 10)
        collider1 = ColliderComponent(ball1, circle1)

        ball2 = Empty()
        circle2 = Circle(None, 10)
        collider2 = ColliderComponent(ball2, circle2)
        ball2.rigidbody.transform.position = (-20, 0)

        self.physics_service._force_sync_to_transform(ball2.rigidbody)

        params_list: list[tuple[Point, Point, float, list[ColliderComponent]]] = [
            # Through Multiple
            ((0, 0), (-20, 0), 0, [collider1, collider2]),
            # Through None
            ((20, 0), (40, 0), 0, []),
            # Through One
            ((-20, 0), (-15, 0), 0, [collider2]),
            # Edge of collider
            ((-30, 0), (-40, 0), 0, [collider2]),
            # Just outside collider
            ((-31, 0), (-40, 0), 0, []),
            # Just outside with radius large enough to capture.
            ((-31, 0), (-40, 0), 1, [collider2]),
            # Edge of collider, negative radius
            ((-30, 0), (-40, 0), -1, []),
            # Just inside collider, negative radius
            ((-29, 0), (-40, 0), -1, [collider2]),
        ]

        for i, (start, end, radius, expected_colliders) in enumerate(params_list):
            with self.subTest(i=i):
                query = self.physics_service.cast_ray(start, end, radius, FILTER)

                self.assertEqual(len(query), len(expected_colliders))

                for collider in expected_colliders:
                    self.assertInRay(collider, query)


if __name__ == "__main__":

    unittest.main()
