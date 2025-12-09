from __future__ import annotations

from typing import TYPE_CHECKING
import unittest

from pyrite._rendering.sprite_renderer.sprite_renderer import DefaultSpriteRenderer
from pyrite.camera import Camera, OrthoProjection
from pyrite.transform import Transform

if TYPE_CHECKING:
    from pygame.typing import Point

    type CameraPosition = Point
    type WorldPosition = Point
    type SurfacePosition = Point

CORNER_100X100 = OrthoProjection((0, 0, -1, 100, 100, 2))
CENTER_100X100 = OrthoProjection((-50, -50, -2, 100, 100, 2))

ORIGIN = (0, 0)
TOPLEFT = (0, 0)


class TestDefaultSpriteRenderer(unittest.TestCase):

    def setUp(self) -> None:
        self.renderer = DefaultSpriteRenderer()

    def test_get_surface_position(self) -> None:
        test_params: dict[
            str, tuple[OrthoProjection, CameraPosition, WorldPosition, SurfacePosition]
        ] = {
            "Ortho, corner, 100x100, origin camera, topleft": (
                CORNER_100X100,
                ORIGIN,
                ORIGIN,
                TOPLEFT,
            ),
            "Ortho, corner, 100x100, origin camera, center": (
                CORNER_100X100,
                ORIGIN,
                (50, -50),
                (50, 50),
            ),
            "Ortho, Center, 100x100, origin camera, topleft": (
                CENTER_100X100,
                ORIGIN,
                (-50, 50),
                (TOPLEFT),
            ),
            "Ortho, Center, 100x100, origin camera, center": (
                CENTER_100X100,
                ORIGIN,
                ORIGIN,
                (50, 50),
            ),
        }

        for case, (
            projection,
            camera_pos,
            world_pos,
            expected_pos,
        ) in test_params.items():
            with self.subTest(i=case):
                camera = Camera(projection, camera_pos)

                surface_pos = self.renderer._get_surface_pos(
                    camera, Transform.from_2d(world_pos)
                )

                self.assertEqual(surface_pos, expected_pos)


if __name__ == "__main__":
    unittest.main()
