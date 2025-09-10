from __future__ import annotations

import unittest

from pyrite.physics import ColliderComponent, RigidbodyComponent
from pyrite.physics.shapes import Circle
from pyrite.services import PhysicsService
from pyrite.services.physics_service import PymunkPhysicsService
from pyrite.transform import TransformComponent


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
        pass

    def test_force_sync_to_transform(self):
        pass

    def test_get_updated_transforms(self):
        pass


if __name__ == "__main__":

    unittest.main()
