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


CENTERED_PROJECTION = OrthoProjection(((-50, -50, 100, 100), -1, 2))
CENTERED_CAMERA = Camera(CENTERED_PROJECTION)
"""
Camera with a centered projection, with world position == (0, 0)
"""

ORIGIN: Point = (0, 0)
SCREEN_CENTER: Point = (50, 50)

Viewport.DEFAULT._update_display_rect((100, 100))


class TestScreenToWorld(unittest.TestCase):

    def test_screen_to_world(self) -> None:
        test_params: dict[str, tuple[Camera, Viewport, ScreenPoint, WorldPoint]] = {
            "CenteredCam, default Viewport": (
                CENTERED_CAMERA,
                Viewport.DEFAULT,
                SCREEN_CENTER,
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
                world_point = camera.to_world(local_mouse_pos)

                self.assertEqual(expected_point, world_point.position)


class TestWorldToScreen(unittest.TestCase):

    def test_world_to_screen(self) -> None:
        test_params: dict[str, tuple[Camera, Viewport, ScreenPoint, WorldPoint]] = {
            "CenteredCam, default Viewport": (
                CENTERED_CAMERA,
                Viewport.DEFAULT,
                SCREEN_CENTER,
                ORIGIN,
            )
        }

        for case, (
            camera,
            viewport,
            expected_point,
            world_point,
        ) in test_params.items():
            with self.subTest(i=case):
                world_transform = Transform.from_2d(world_point)
                eye_pos = camera.to_eye(camera.to_local(world_transform)).position
                ndc_pos = camera.projection.eye_to_ndc(Transform.from_2d(eye_pos))
                screen_pos = viewport.ndc_to_screen(ndc_pos)

                self.assertEqual(expected_point, screen_pos)


if __name__ == "__main__":
    unittest.main()
