from __future__ import annotations
import math
import pathlib
import sys
import unittest

from pygame import Vector2

sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.collider.ellipse import EllipseCollider  # noqa:E402
from src.pyrite.transform import Transform  # noqa:E402


class TestCollider(unittest.TestCase):

    def setUp(self):
        self.circle1 = EllipseCollider(5)
        self.circle2 = EllipseCollider(4)
        self.transform1 = Transform((1, 2))
        self.transform2 = Transform((5, 5))

    def test_gjk_support(self):

        # Cardinal direction, no rotation
        direction = Vector2(1, 0)

        result = self.circle1._gjk_support_function(direction, self.transform1)
        self.assertEqual(result, Vector2(6, 2))

        result = self.circle2._gjk_support_function(direction, self.transform2)
        self.assertEqual(result, Vector2(9, 5))

        # Orthoginal from past, no rotation
        direction = Vector2(0, 1)

        result = self.circle1._gjk_support_function(direction, self.transform1)
        self.assertEqual(result, Vector2(1, 7))

        result = self.circle2._gjk_support_function(direction, self.transform2)
        self.assertEqual(result, Vector2(5, 9))

        # Rotated direction vector, no transform rotation
        direction = Vector2(1, 0).rotate(45)

        result = self.circle1._gjk_support_function(direction, self.transform1)
        angle = math.cos(math.radians(45))
        expected = Vector2(
            (angle * 5) + self.transform1.position.x,
            (angle * 5) + self.transform1.position.y,
        )
        self.assertAlmostEqual(result.x, expected.x)
        self.assertAlmostEqual(result.y, expected.y)

        # Cardinal direction, rotation of transform
        # Rotating by given amount should be equivalent to rotating vector opposite way
        transform3 = Transform((1, 2), -45)
        direction = Vector2(1, 0)

        result = self.circle1._gjk_support_function(direction, transform3)
        angle = math.cos(math.radians(45))
        expected = Vector2(
            (angle * 5) + self.transform1.position.x,
            (angle * 5) + self.transform1.position.y,
        )
        self.assertAlmostEqual(result.x, expected.x)
        self.assertAlmostEqual(result.y, expected.y)


if __name__ == "__main__":

    unittest.main()
