from __future__ import annotations

# import math
import pathlib
import sys
import unittest

from pygame import Vector2

sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.collider.ellipse import EllipseCollider  # noqa:E402
from src.pyrite.collider.collider_system import ColliderSystem  # noqa:E402
from src.pyrite.collider import collider_system  # noqa:E402
from src.pyrite.transform import Transform  # noqa:E402


class TestColliserSystem(unittest.TestCase):

    def setUp(self) -> None:
        self.collider1 = EllipseCollider(5)
        self.collider2 = EllipseCollider(4)

    def test_support_function(self):
        direction = Vector2(1, 0)

        transform1 = Transform((5, 5))
        transform2 = Transform((-4, -4))

        sp1 = ColliderSystem.support_function(
            direction, self.collider1, self.collider2, transform1, transform2
        )

        self.assertEqual(sp1, Vector2(18, 9))

    def test_normal(self):
        point_a = Vector2(-3, -4)
        point_b = Vector2(3, -2)
        normal = ColliderSystem.get_normal(point_a, point_b)
        edge = point_a - point_b

        self.assertEqual(edge, Vector2(-6, -2))

        self.assertEqual(normal, Vector2(-edge.y, edge.x))

    def test_check_region(self):

        region1 = [Vector2(1, 1), Vector2(-1, 1), Vector2(0, -1)]

        self.assertTrue(collider_system.check_region(region1))

        region2 = [Vector2(1, 1), Vector2(-1, 1), Vector2(0, 2)]

        self.assertFalse(collider_system.check_region(region2))

        # Same triangle as 1, opposing chirality

        region3 = [Vector2(-1, 1), Vector2(1, 1), Vector2(0, -1)]

        self.assertTrue(collider_system.check_region(region3))

        # Needs addt'l edge cases
        # Literal origin on edge, vertex on origin

        # Origin on vertex
        region4 = [Vector2(1, 1), Vector2(-1, 1), Vector2(0, 0)]

        self.assertFalse(collider_system.check_region(region4))

        # Origin on edge
        region5 = [Vector2(-1, 0), Vector2(1, 0), Vector2(0, 1)]

        self.assertTrue(collider_system.check_region(region5))

    def test_collide(self):
        collider_a = EllipseCollider(5)
        collider_b = EllipseCollider(4)

        transform_a = Transform((5, 5))
        transform_b = Transform((-4, -4))

        # Obviously no overlap
        self.assertFalse(
            ColliderSystem.collide(collider_a, collider_b, transform_a, transform_b)
        )

        transform_c = Transform((0, 0))

        # This SHOULD overlap
        self.assertTrue(
            ColliderSystem.collide(collider_a, collider_b, transform_a, transform_c)
        )


if __name__ == "__main__":

    unittest.main()
