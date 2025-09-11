from __future__ import annotations

import math
import unittest

from pyrite.physics import ColliderComponent, RigidbodyComponent
from pyrite.physics.shapes import Circle
from pyrite.services import PhysicsService
from pyrite.services.physics_service import PymunkPhysicsService
from pyrite.transform import TransformComponent, Transform


class Empty:

    def __init__(self) -> None:
        self.transform = TransformComponent(self)
        self.rigidbody = RigidbodyComponent(self)


class TestPymunkPhysicsService(unittest.TestCase):

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


if __name__ == "__main__":

    unittest.main()
