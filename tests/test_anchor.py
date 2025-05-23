from __future__ import annotations
import pathlib
import sys
import unittest

from pygame import Rect


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


if __name__ == "__main__":

    unittest.main()
