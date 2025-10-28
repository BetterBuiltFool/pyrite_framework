from __future__ import annotations

from typing import TYPE_CHECKING
import unittest

from pygame import Vector2

from pyrite._camera.camera import BaseCamera
from pyrite._camera.ortho_projection import OrthoProjection
from pyrite._rendering.viewport import Viewport

if TYPE_CHECKING:
    from pygame.typing import Point

    type ScreenPoint = Point
    type LocalPoint = Point

CAMERA = BaseCamera(OrthoProjection((-50, -50, 100, 100)))
Viewport.DEFAULT._update_display_rect((100, 100))

# Represents the top left quarter of the screen.
TOPLEFT_QUADRANT_VIEW = Viewport((-1, 1, 1, 1))
TOPLEFT_QUADRANT_VIEW._update_display_rect((100, 100))


class TestBaseCamera(unittest.TestCase):

    def test_get_mouse_position(self) -> None:
        params: dict[str, tuple[BaseCamera, Viewport, ScreenPoint, LocalPoint]] = {
            "Centered mouse": (CAMERA, Viewport.DEFAULT, (50, 50), (0, 0)),
            "Topleft mouse": (CAMERA, Viewport.DEFAULT, (0, 0), (-50, 50)),
            "Bottomright mouse": (CAMERA, Viewport.DEFAULT, (100, 100), (50, -50)),
            "Centered TL Quad": (CAMERA, TOPLEFT_QUADRANT_VIEW, (50, 50), ((50, -50))),
        }

        for case, (camera, viewport, mouse_pos, expected_pos) in params.items():
            with self.subTest(i=case):
                local_pos = camera._get_mouse_position(viewport, mouse_pos)

                self.assertEqual(expected_pos, Vector2(local_pos))


if __name__ == "__main__":
    unittest.main()
