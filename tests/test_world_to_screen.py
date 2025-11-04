"""
Integration test between camera/DefaultCameraService, Viewport, and OrthoProjection to
ensure that a screen points and world point can correctly be transformed into eachother.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
import unittest

from pyrite.camera import Camera, OrthoProjection
from pyrite.rendering import Viewport
from pyrite.transform import Transform


if TYPE_CHECKING:
    from pygame.typing import Point

    type ScreenPoint = Point
    type WorldPoint = Point


CENTERED_PROJECTION = OrthoProjection((-50, -50, 100, 100), -1, 1)
CENTERED_CAMERA = Camera(CENTERED_PROJECTION)
"""
Camera with a centered projection, with world position == (0, 0)
"""

ORIGIN: Point = (0, 0)

Viewport.DEFAULT._update_display_rect((100, 100))


class TestScreenToWorld(unittest.TestCase):

    def test_screen_to_world(self) -> None:
        test_params: dict[str, tuple[Camera, Viewport, ScreenPoint, WorldPoint]] = {
            "CenteredCam, default Viewport": (
                CENTERED_CAMERA,
                Viewport.DEFAULT,
                ORIGIN,
                ORIGIN,
            )
        }

        for case, (
            camera,
            viewport,
            screen_point,
            expected_point,
        ) in test_params.items():
            with self.subTest(i=case):
                local_mouse_pos = camera._get_mouse_position(viewport, screen_point)
                world_point = camera.to_world(Transform(local_mouse_pos))

                self.assertEqual(expected_point, world_point.position)


class TestWorldToScreen(unittest.TestCase):

    def test_world_to_screen(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
