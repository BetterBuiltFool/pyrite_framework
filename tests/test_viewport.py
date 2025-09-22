from __future__ import annotations

from typing import TYPE_CHECKING
import unittest

from pygame import FRect, Rect

from pyrite._rendering.viewport import Viewport

if TYPE_CHECKING:
    from pygame.typing import Point

    type NDCCoords = Point
    type ScreenCoords = Point

display_size: Point = (600, 800)


fullscreen = FRect(-1, 1, 2, 2)
lower_right = FRect(-1, 1, 1, 1)
bottom_right = FRect(0, 0, 1, 1)
upper_left = FRect(-1, 1, 1, 1)

screen_center = (display_size[0] / 2, display_size[1] / 2)


class TestViewport(unittest.TestCase):

    def test_get_subrect(self):

        test_params: dict[str, tuple[FRect, Rect]] = {
            "Full screen": (fullscreen, Rect(0, 0, 600, 800)),
            "Lower Right": (lower_right, Rect(0, 0, 300, 400)),
            "Upper left": (upper_left, Rect(0, 0, 300, 400)),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                display = (600, 800)
                viewport_rect, expected_rect = params

                display_rect = Viewport._get_subrect(viewport_rect, display)

                self.assertEqual(display_rect, expected_rect)

    def test_ndc_to_screen(self):

        test_params: dict[str, tuple[FRect, NDCCoords, ScreenCoords]] = {
            "Full screen, top left point": (fullscreen, (-1, 1), (0, 0)),
            "Full screen, bottom right point": (fullscreen, (1, -1), display_size),
            "Full screen, center point": (
                fullscreen,
                (0, 0),
                screen_center,
            ),
            "Bottomright quadrant screen, top left point": (
                bottom_right,
                (-1, 1),
                screen_center,
            ),
            "Bottomright quadrant screen, bottom right point": (
                bottom_right,
                (1, -1),
                display_size,
            ),
            "Bottomright quadrant screen, center point": (
                bottom_right,
                (0, 0),
                (3 * display_size[0] / 4, 3 * display_size[1] / 4),
            ),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                viewport_rect, ndc_coords, expected_coords = params
                viewport = Viewport(viewport_rect)
                viewport._update_display_rect(display_size)

                screen_coords = viewport.ndc_to_screen(ndc_coords)

                self.assertEqual(screen_coords, expected_coords)

    def test_screen_to_ndc(self):

        test_params: dict[str, tuple[FRect, ScreenCoords, NDCCoords]] = {
            "Full screen, top left point": (fullscreen, (0, 0), (-1, 1)),
            "Full screen, bottom right point": (fullscreen, display_size, (1, -1)),
            "Full screen, center point": (fullscreen, screen_center, (0, 0)),
            "Bottomright quadrant screen, top left point": (
                bottom_right,
                screen_center,
                (-1, 1),
            ),
            "Bottomright quadrant screen, bottom right point": (
                bottom_right,
                display_size,
                (1, -1),
            ),
            "Bottomright quadrant screen, center point": (
                bottom_right,
                (3 * display_size[0] / 4, 3 * display_size[1] / 4),
                (0, 0),
            ),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                viewport_rect, screen_coords, expected_coords = params
                viewport = Viewport(viewport_rect)
                viewport._update_display_rect(display_size)

                ndc_coords = viewport.screen_to_ndc(screen_coords)

                self.assertEqual(ndc_coords, expected_coords)


if __name__ == "__main__":
    unittest.main()
