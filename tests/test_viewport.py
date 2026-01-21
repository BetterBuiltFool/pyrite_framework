from __future__ import annotations

from typing import TYPE_CHECKING
import unittest

import glm
from pygame import FRect, Rect, Vector3

from pyrite._rendering.viewport import Viewport
from pyrite._transform.transform import Transform

if TYPE_CHECKING:
    from pygame.typing import Point
    from pyrite.types import Point3D

    type NDCCoords = Point3D
    type ScreenCoords = Point

display_size: Point = (600, 800)


fullscreen = FRect(-1, 1, 2, 2)
lower_right = FRect(-1, 1, 1, 1)
bottom_right = FRect(0, 0, 1, 1)
upper_left = FRect(-1, 1, 1, 1)

SCREEN_CENTER: ScreenCoords = (display_size[0] / 2, display_size[1] / 2)
ORIGIN_3D: NDCCoords = (0, 0, 0)
TOPLEFT: ScreenCoords = (0, 0)


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

    def test_clip_to_viewport(self):

        test_params: dict[str, tuple[FRect, NDCCoords, ScreenCoords]] = {
            "Full screen, top left point": (fullscreen, (-1, 1, 0), TOPLEFT),
            "Full screen, bottom right point": (fullscreen, (1, -1, 0), display_size),
            "Full screen, center point": (
                fullscreen,
                ORIGIN_3D,
                SCREEN_CENTER,
            ),
            "Bottomright quadrant screen, top left point": (
                bottom_right,
                (-1, 1, 0),
                SCREEN_CENTER,
            ),
            "Bottomright quadrant screen, bottom right point": (
                bottom_right,
                (1, -1, 0),
                display_size,
            ),
            "Bottomright quadrant screen, center point": (
                bottom_right,
                ORIGIN_3D,
                (3 * display_size[0] / 4, 3 * display_size[1] / 4),
            ),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                viewport_rect, ndc_coords, expected_coords = params
                viewport = Viewport(viewport_rect)
                viewport._update_display_rect(display_size)

                clip_coords = Transform.from_2d(Vector3(ndc_coords).xy)
                screen_coords = viewport.clip_to_viewport(clip_coords)

                self.assertEqual(screen_coords.position, expected_coords)

    def test_viewport_to_clip(self):

        test_params: dict[str, tuple[FRect, ScreenCoords, NDCCoords]] = {
            "Full screen, top left point": (fullscreen, TOPLEFT, (-1, 1, 0)),
            "Full screen, bottom right point": (fullscreen, display_size, (1, -1, 0)),
            "Full screen, center point": (fullscreen, SCREEN_CENTER, ORIGIN_3D),
            "Bottomright quadrant screen, top left point": (
                bottom_right,
                SCREEN_CENTER,
                (-1, 1, 0),
            ),
            "Bottomright quadrant screen, bottom right point": (
                bottom_right,
                display_size,
                (1, -1, 0),
            ),
            "Bottomright quadrant screen, center point": (
                bottom_right,
                (3 * display_size[0] / 4, 3 * display_size[1] / 4),
                ORIGIN_3D,
            ),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                viewport_rect, screen_coords, expected_coords = params
                viewport = Viewport(viewport_rect)
                viewport._update_display_rect(display_size)

                ndc_coords = viewport.viewport_to_clip(screen_coords)

                self.assertEqual(ndc_coords, Transform(glm.vec3(*expected_coords)))


if __name__ == "__main__":
    unittest.main()
