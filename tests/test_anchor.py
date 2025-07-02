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
anchor_75x_5y: Point = (0.75, 0.5)
anchor_5x_75y: Point = (0.5, 0.75)
anchor_quarter: Point = (0.25, 0.25)

rect_size: RectLike = (0, 0, 8, 4)

default_scale: Point = (1, 1)


class TestAnchor(unittest.TestCase):

    def test_get_center_offset(self):
        test_params: dict[str, tuple[Point, RectLike, Point]] = {
            "Center Anchor": (anchor_center, rect_size, (0, 0)),
            "Center X, 3/4 Y": (anchor_5x_75y, rect_size, (0, 1)),
            "3/4 X, Center Y": (anchor_75x_5y, rect_size, (2, 0)),
            "1/4 X, 1/4 Y": (anchor_quarter, rect_size, (-2, -1)),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                anchor = Anchor(params[0])
                rect = Rect(params[1])
                expected = Vector2(params[2])

                pivot = anchor.get_center_offset(rect)

                self.assertEqual(pivot, expected)

    def test_get_rect_center(self):
        test_params: dict[str, tuple[Point, float, Point, Point]] = {
            "Case: (Center X, Center Y), 0 C": (
                anchor_center,
                0,
                default_scale,
                (6, -2),
            ),
            "Case: (3/4 X, Center Y), 0 C": (
                anchor_75x_5y,
                0,
                default_scale,
                (4, -2),
            ),
            "Case: (3/4 X, Center Y), 90 C": (
                anchor_75x_5y,
                90,
                default_scale,
                (6, -4),
            ),
            "Case: (3/4 X, Center Y), -90 C": (
                anchor_75x_5y,
                -90,
                default_scale,
                (6, 0),
            ),
            "Case: (3/4 X, Center Y), 180 C": (
                anchor_75x_5y,
                180,
                default_scale,
                (8, -2),
            ),
            "Case: (3/4 X, Center Y), 0 C, (2,2) scale": (
                anchor_75x_5y,
                0,
                (2, 2),
                (2, -2),
            ),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                rect = Rect(rect_size)
                anchor = Anchor(params[0])
                angle = params[1]
                scale = params[2]
                expected = Vector2(params[3])

                new_center = anchor.get_rect_center(rect, (6, -2), angle, scale)

                self.assertEqual(new_center, expected)


if __name__ == "__main__":

    unittest.main()
