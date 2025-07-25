from __future__ import annotations

import unittest

from pygame import Rect

from pyrite.rendering.rect_bounds import rotate_rect
from pyrite.enum import Anchor


anchor_center = Anchor((0.5, 0.5))
anchor_75x_5y = Anchor((0.75, 0.5))
rect = Rect(-4, -2, 8, 4)


class TestRectBounds(unittest.TestCase):

    def test_rotate_rect(self):

        test_params: dict[str, tuple[Anchor, float, Rect]] = {
            "Centered anchor, 90 rotation": (anchor_center, 90, Rect(-2, -4, 4, 8)),
            "3/4 X, Center Y, 90 rotation": (anchor_75x_5y, 90, Rect(0, -2, 4, 8)),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                anchor, angle, expected = params

                rotated_rect = rotate_rect(rect, angle, anchor.get_center_offset(rect))

                self.assertEqual(rotated_rect, expected)


if __name__ == "__main__":

    unittest.main()
