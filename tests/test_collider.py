from __future__ import annotations
import pathlib
import sys
import unittest

from pygame import Vector2

sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.collider.elipse import ElipseCollider  # noqa:E402
from src.pyrite.transform import Transform  # noqa:E402


class TestCollider(unittest.TestCase):

    def setUp(self):
        self.circle1 = ElipseCollider(5)
        self.circle2 = ElipseCollider(4)
        self.transform1 = Transform((1, 2))
        self.transform2 = Transform((5, 5))

    def test_gjk_support(self):

        direction = Vector2(1, 0)

        result = self.circle1._gjk_support_function(direction, self.transform1)

        self.assertEqual(result, Vector2(6, 2))


if __name__ == "__main__":

    unittest.main()
