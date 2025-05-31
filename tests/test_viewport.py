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

display_size = (600, 800)


def get_display_rect(self: Viewport) -> Rect:
    return self._get_subrect(self.frect, display_size)


class TestViewport(unittest.TestCase):

    def setUp(self) -> None:
        # Some methods use this, so we monkeypatch in a controlled, testable version.
        Viewport.get_display_rect = get_display_rect

    def test_get_subrect(self):
        # Full screen
        display = (600, 800)
        viewport_rect = FRect(-1, 1, 2, 2)

        display_rect = Viewport._get_subrect(viewport_rect, display)

        expected_rect = Rect(0, 0, 600, 800)

        self.assertEqual(display_rect, expected_rect)

        # Lower Right
        viewport_rect = FRect(0, 0, 1, 1)

        display_rect = Viewport._get_subrect(viewport_rect, display)

        expected_rect = Rect(300, 400, 300, 400)

        self.assertEqual(display_rect, expected_rect)

        # Upper left
        viewport_rect = FRect(-1, 1, 1, 1)

        display_rect = Viewport._get_subrect(viewport_rect, display)

        expected_rect = Rect(0, 0, 300, 400)

        self.assertEqual(display_rect, expected_rect)

    def test_ndc_to_screen(self):
        # Full screen, top left point
        viewport_rect = FRect(-1, 1, 2, 2)
        viewport = Viewport(viewport_rect)
        ndc_coords = (-1, 1)

        screen_coords = viewport.ndc_to_screen(ndc_coords)

        expected_coords = (0, 0)

        self.assertEqual(screen_coords, expected_coords)

        # Full screen, bottom right point
        ndc_coords = (1, -1)

        screen_coords = viewport.ndc_to_screen(ndc_coords)

        expected_coords = display_size

        self.assertEqual(screen_coords, expected_coords)

        # Full screen, center point
        ndc_coords = (0, 0)

        screen_coords = viewport.ndc_to_screen(ndc_coords)

        expected_coords = display_size[0] / 2, display_size[1] / 2

        self.assertEqual(screen_coords, expected_coords)

        # Bottomright quadrant screen, top left point
        viewport_rect = FRect(0, 0, 1, 1)
        viewport = Viewport(viewport_rect)
        ndc_coords = (-1, 1)

        screen_coords = viewport.ndc_to_screen(ndc_coords)

        expected_coords = display_size[0] / 2, display_size[1] / 2

        self.assertEqual(screen_coords, expected_coords)

        # Bottomright quadrant screen, bottom right point
        ndc_coords = (1, -1)

        screen_coords = viewport.ndc_to_screen(ndc_coords)

        expected_coords = display_size

        self.assertEqual(screen_coords, expected_coords)

        # Bottomright quadrant screen, center point
        ndc_coords = (0, 0)

        screen_coords = viewport.ndc_to_screen(ndc_coords)

        expected_coords = 3 * display_size[0] / 4, 3 * display_size[1] / 4

        self.assertEqual(screen_coords, expected_coords)

    def test_screen_to_ndc(self):
        # Full screen, top left point
        viewport_rect = FRect(-1, 1, 2, 2)
        viewport = Viewport(viewport_rect)
        screen_coords = (0, 0)

        ndc_coords = viewport.screen_to_ndc(screen_coords)

        expected_coords = (-1, 1)

        self.assertEqual(ndc_coords, expected_coords)

        # Full screen, bottom right point
        screen_coords = display_size

        ndc_coords = viewport.screen_to_ndc(screen_coords)

        expected_coords = (1, -1)

        self.assertEqual(ndc_coords, expected_coords)

        # Full screen, center point
        screen_coords = display_size[0] / 2, display_size[1] / 2

        ndc_coords = viewport.screen_to_ndc(screen_coords)

        expected_coords = (0, 0)

        self.assertEqual(ndc_coords, expected_coords)

        # Bottomright quadrant screen, top left point
        viewport_rect = FRect(0, 0, 1, 1)
        viewport = Viewport(viewport_rect)
        screen_coords = display_size[0] / 2, display_size[1] / 2

        ndc_coords = viewport.screen_to_ndc(screen_coords)

        expected_coords = (-1, 1)

        self.assertEqual(ndc_coords, expected_coords)

        # Bottomright quadrant screen, bottom right point
        screen_coords = display_size

        ndc_coords = viewport.screen_to_ndc(screen_coords)

        expected_coords = (1, -1)

        self.assertEqual(ndc_coords, expected_coords)

        # Bottomright quadrant screen, center point
        screen_coords = 3 * display_size[0] / 4, 3 * display_size[1] / 4

        ndc_coords = viewport.screen_to_ndc(screen_coords)

        expected_coords = (0, 0)

        self.assertEqual(ndc_coords, expected_coords)


if __name__ == "__main__":
    unittest.main()
