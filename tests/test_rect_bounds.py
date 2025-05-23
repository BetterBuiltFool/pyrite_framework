from __future__ import annotations
import pathlib
import sys
import unittest

from pygame import Rect


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.rendering.rect_bounds import rotate_rect  # noqa:E402
from src.pyrite.enum import Anchor  # noqa:E402


class TestRectBounds(unittest.TestCase):

    def test_rotate_rect(self):
        # Centered anchor, 90 rotation.
        anchor = Anchor((0.5, 0.5))

        rect = Rect(-4, -2, 8, 4)

        rotated_rect = rotate_rect(rect, 90, anchor.get_center_offset(rect))

        self.assertEqual(rotated_rect.left, -2)
        self.assertEqual(rotated_rect.top, -4)
        self.assertEqual(rotated_rect.width, 4)
        self.assertEqual(rotated_rect.height, 8)

        # 3/4 X, Center Y, 90 rotation.
        anchor = Anchor((0.75, 0.5))

        rect = Rect(-4, -2, 8, 4)

        rotated_rect = rotate_rect(rect, 90, anchor.get_center_offset(rect))

        self.assertEqual(rotated_rect.left, 0)
        self.assertEqual(rotated_rect.top, -6)
        self.assertEqual(rotated_rect.width, 4)
        self.assertEqual(rotated_rect.height, 8)


if __name__ == "__main__":

    unittest.main()
