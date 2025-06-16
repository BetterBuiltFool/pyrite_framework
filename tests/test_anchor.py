from __future__ import annotations
import pathlib
import sys
import unittest

from pygame import Rect, Vector2


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.enum import Anchor  # noqa:E402


class TestAnchor(unittest.TestCase):

    def test_get_center_offset(self):
        # Center anchor
        anchor = Anchor((0.5, 0.5))
        rect = Rect(0, 0, 8, 4)

        pivot = anchor.get_center_offset(rect)

        self.assertEqual(pivot.x, 0)
        self.assertEqual(pivot.y, 0)

        # Center X, 3/4 Y

        anchor = Anchor((0.5, 0.75))

        pivot = anchor.get_center_offset(rect)

        self.assertEqual(pivot.x, 0)
        self.assertEqual(pivot.y, 1)

        # 3/4 X, Center Y

        anchor = Anchor((0.75, 0.5))

        pivot = anchor.get_center_offset(rect)

        self.assertEqual(pivot.x, 2)
        self.assertEqual(pivot.y, 0)

        # 1/4 X, 1/4 Y

        anchor = Anchor((0.25, 0.25))

        pivot = anchor.get_center_offset(rect)

        self.assertEqual(pivot.x, -2)
        self.assertEqual(pivot.y, -1)

    def test_get_rect_center(self):
        # Case: (Center X, Center Y), 0 C
        rect = Rect(0, 0, 8, 4)
        anchor = Anchor((0.5, 0.5))
        angle = 0

        new_center = anchor.get_rect_center(rect, (6, -2), angle)

        expected = Vector2(6, -2)

        self.assertEqual(new_center, expected)

        # Case: (3/4 X, Center Y), 0 C
        anchor = Anchor((0.75, 0.5))
        angle = 0

        new_center = anchor.get_rect_center(rect, (6, -2), angle)

        expected = Vector2(4, -2)

        self.assertEqual(new_center, expected)

        # Case: (3/4 X, Center Y), 90 C
        angle = 90

        new_center = anchor.get_rect_center(rect, (6, -2), angle)

        expected = Vector2(6, -4)

        self.assertEqual(new_center, expected)

        # Case: (3/4 X, Center Y), -90 C
        angle = -90

        new_center = anchor.get_rect_center(rect, (6, -2), angle)

        expected = Vector2(6, 0)

        self.assertEqual(new_center, expected)

        # Case: (3/4 X, Center Y), 180 C
        angle = 180

        new_center = anchor.get_rect_center(rect, (6, -2), angle)

        expected = Vector2(8, -2)

        self.assertEqual(new_center, expected)

        # Case: (3/4 X, Center Y), 0 C, (2,2) scale
        angle = 0
        scale = (2, 2)

        new_center = anchor.get_rect_center(rect, (6, -2), angle, scale)

        expected = Vector2(2, -2)

        self.assertEqual(new_center, expected)


if __name__ == "__main__":

    unittest.main()
