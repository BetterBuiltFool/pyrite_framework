from __future__ import annotations
from typing import cast, TYPE_CHECKING
import unittest

import glm
from pygame import Vector3

from pyrite.rendering import Viewport
from pyrite._services.camera_service import CameraServiceProvider as CameraService
from pyrite._services.camera_service.camera_service import DefaultCameraService
from pyrite.camera import OrthoProjection
from pyrite._types.projection import Projection
from pyrite._types.camera import Camera
from pyrite.transform import TransformComponent, Transform

if TYPE_CHECKING:
    from pygame.typing import Point

    type WorldCoords = Vector3
    type LocalCoords = Vector3
    type NDCCoords = Vector3
    type ZoomLevel = float
    type WorldTransform = Transform
    type LocalTransform = Transform
    type EyeTransform = Transform
    type ScreenPoint = Point


centered_projection = OrthoProjection(((-400, -300, 800, 600), -1, 2))
three_quart_projection = OrthoProjection(((-200, -150, 800, 600), -1, 2))
zero_vector = Vector3(0, 0, 0)
zero_transform = Transform()
ORIGIN: WorldCoords = Vector3(0, 0, 0)
SCREEN_CENTER: Point = (50, 50)

Viewport.DEFAULT._update_display_rect((100, 100))


class MockCamera:

    def __new__(cls, *args, **kwds) -> Camera:
        return cast(Camera, super().__new__(cls))

    def __init__(self, projection: Projection) -> None:
        self.projection = projection
        self.transform: TransformComponent = TransformComponent(self)
        self.zoom_level: ZoomLevel = 1
        CameraService.add_camera(cast(Camera, self))


class TestCameraService(unittest.TestCase):

    def test_world_to_clip(self):
        test_params: dict[
            str, tuple[OrthoProjection, WorldCoords, NDCCoords, ZoomLevel]
        ] = {
            "Centered projection, center coords": (
                centered_projection,
                zero_vector,
                zero_vector,
                1,
            ),
            "Centered projection, topleft corner coords": (
                centered_projection,
                Vector3(-400, 300, 1),
                Vector3(-1, 1, 1),
                1,
            ),
            "3/4 projection, 0 coords": (
                three_quart_projection,
                zero_vector,
                Vector3(-0.5, 0.5, 0),
                1,
            ),
            "3/4 projection, center coords": (
                three_quart_projection,
                Vector3(200, -150, 0),
                zero_vector,
                1,
            ),
            "3/4 projection, topleft corner coords": (
                three_quart_projection,
                Vector3(-200, 150, 0),
                Vector3(-1, 1, 0),
                1,
            ),
            "Centered projection, center coords, zoom level 2": (
                centered_projection,
                zero_vector,
                zero_vector,
                2,
            ),
            "Centered projection, topleft corner coords, zoom level 2": (
                centered_projection,
                Vector3(-200, 150, 1),
                Vector3(-1, 1, 1),
                2,
            ),
        }

        CameraService._service = cast(DefaultCameraService, CameraService._service)
        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                projection, world_position, expected, zoom_level = params
                test_cam = MockCamera(projection.zoom(zoom_level))
                ndc_coords = CameraService._service.world_to_clip(
                    test_cam, Transform(glm.vec3(*world_position))
                )

                self.assertEqual(ndc_coords.position_3d, expected)

    def test_clip_to_world(self) -> None:
        test_params: dict[
            str, tuple[OrthoProjection, WorldCoords, NDCCoords, ZoomLevel]
        ] = {
            "Centered projection, center coords": (
                centered_projection,
                zero_vector,
                zero_vector,
                1,
            ),
            "Centered projection, topleft corner coords": (
                centered_projection,
                Vector3(-400, 300, 1),
                Vector3(-1, 1, 1),
                1,
            ),
            "3/4 projection, 0 coords": (
                three_quart_projection,
                zero_vector,
                Vector3(-0.5, 0.5, 0),
                1,
            ),
            "3/4 projection, center coords": (
                three_quart_projection,
                Vector3(200, -150, 0),
                zero_vector,
                1,
            ),
            "3/4 projection, topleft corner coords": (
                three_quart_projection,
                Vector3(-200, 150, 0),
                Vector3(-1, 1, 0),
                1,
            ),
            "Centered projection, center coords, zoom level 2": (
                centered_projection,
                zero_vector,
                zero_vector,
                2,
            ),
            "Centered projection, topleft corner coords, zoom level 2": (
                centered_projection,
                Vector3(-200, 150, 1),
                Vector3(-1, 1, 1),
                2,
            ),
        }

        CameraService._service = cast(DefaultCameraService, CameraService._service)
        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                projection, expected, clip_coords, zoom_level = params
                test_cam = MockCamera(projection.zoom(zoom_level))
                world_coords = CameraService._service.clip_to_world(
                    test_cam, Transform(glm.vec3(*clip_coords))
                )

                self.assertEqual(world_coords.position_3d, expected)

    def test_world_to_screen(self) -> None:
        test_params: dict[
            str, tuple[Projection, Viewport, ScreenPoint, WorldCoords]
        ] = {
            "Centered projection, default Viewport": (
                centered_projection,
                Viewport.DEFAULT,
                SCREEN_CENTER,
                ORIGIN,
            )
        }

        for case, (
            projection,
            viewport,
            expected_point,
            world_point,
        ) in test_params.items():
            with self.subTest(i=case):
                test_cam = MockCamera(projection)
                screen_pos = CameraService.world_to_screen(
                    world_point, test_cam, viewport
                )

                self.assertEqual(expected_point, screen_pos)


if __name__ == "__main__":

    unittest.main()
