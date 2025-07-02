from __future__ import annotations
import pathlib
import sys
from typing import TYPE_CHECKING
import unittest

from pygame import Rect, Vector2

if TYPE_CHECKING:
    from pygame.typing import Point, RectLike


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.enum import Anchor  # noqa:E402

anchor_center: Point = (0.5, 0.5)
rect_size: RectLike = (0, 0, 8, 4)


class TestAnchor(unittest.TestCase):

    def get_center_offset(
        self, anchor_point: Point, rect_size: RectLike, expected: Point
    ):
        anchor = Anchor(anchor_point)
        rect = Rect(rect_size)
        pivot = anchor.get_center_offset(rect)

        expected_vector = Vector2(expected)

        self.assertEqual(pivot, expected_vector)

    def test_get_center_offset(self):
        test_params: list[tuple[Point, RectLike, Point]] = [
            # Center Anchor
            (anchor_center, rect_size, (0, 0)),
            # Center X, 3/4 Y
            ((0.5, 0.75), rect_size, (0, 1)),
            # 3/4 X, Center Y
            ((0.75, 0.5), rect_size, (2, 0)),
            # 1/4 X, 1/4 Y
            ((0.25, 0.25), rect_size, (-2, -1)),
        ]

        for params in test_params:
            self.get_center_offset(*params)

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
