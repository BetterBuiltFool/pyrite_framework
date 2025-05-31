from __future__ import annotations

import pathlib
import sys
from typing import TYPE_CHECKING
import unittest

from pygame import FRect, Rect

if TYPE_CHECKING:
    pass

sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.rendering.viewport import Viewport  # noqa:E402


class TestViewport(unittest.TestCase):

    def test_get_subrect(self):
        display = (600, 800)
        viewport_rect = FRect(-1, 1, 2, 2)

        display_rect = Viewport._get_subrect(viewport_rect, display)

        expected_rect = Rect(0, 0, 600, 800)

        self.assertEqual(display_rect, expected_rect)

        viewport_rect = FRect(0, 0, 1, 1)

        display_rect = Viewport._get_subrect(viewport_rect, display)

        expected_rect = Rect(300, 400, 300, 400)

        self.assertEqual(display_rect, expected_rect)

        viewport_rect = FRect(-1, 1, 1, 1)

        display_rect = Viewport._get_subrect(viewport_rect, display)

        expected_rect = Rect(0, 0, 300, 400)

        self.assertEqual(display_rect, expected_rect)


if __name__ == "__main__":
    unittest.main()
