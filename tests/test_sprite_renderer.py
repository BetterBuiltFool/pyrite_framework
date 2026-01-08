from __future__ import annotations

from typing import cast, TYPE_CHECKING
import unittest

from pyrite._rendering.sprite_renderer.sprite_renderer import DefaultSpriteRenderer
from pyrite._services.camera_service import CameraServiceProvider as CameraService
from pyrite._services.camera_service.camera_service import DefaultCameraService
from pyrite.camera import Camera, OrthoProjection
from pyrite.transform import Transform

if TYPE_CHECKING:
    from typing import Any

    from pygame.typing import Point

    type CameraPosition = Point
    type WorldPosition = Point
    type SurfacePosition = Point

CORNER_100X100 = OrthoProjection((0, 0, 0, 100, 100, 2))
CENTER_100X100 = OrthoProjection((-50, -50, -1, 100, 100, 2))

ORIGIN: WorldPosition = (0, 0)
TOPLEFT: SurfacePosition = (0, 0)


class TestDefaultSpriteRenderer(unittest.TestCase):

    def assertAlmostEqualVector2(
        self,
        first: Point,
        second: Point,
        places: int | None = None,
        msg: Any = None,
        delta: None = None,
    ) -> None:

        self.assertAlmostEqual(first[0], second[0], places, msg, delta)
        self.assertAlmostEqual(first[1], second[1], places, msg, delta)

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

                camera_service = cast(DefaultCameraService, CameraService._service)

                surface = camera_service._surfaces[camera]

                world_transform = Transform.from_2d(world_pos)

                surface_pos = self.renderer._get_surface_pos(
                    camera, world_transform, surface.get_rect()
                )

                self.assertAlmostEqualVector2(surface_pos, expected_pos, 1)


if __name__ == "__main__":
    unittest.main()
