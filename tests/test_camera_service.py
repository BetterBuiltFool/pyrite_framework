from __future__ import annotations
from typing import cast, TYPE_CHECKING
import unittest

from pygame import Rect, Vector3

from pyrite.services import CameraService
from pyrite._rendering import OrthoProjection
from pyrite.types.projection import Projection
from pyrite.types.camera import CameraBase
from pyrite.transform import TransformComponent, Transform

if TYPE_CHECKING:

    type LocalCoords = Vector3
    type NDCCoords = Vector3
    type ZoomLevel = float
    type WorldTransform = Transform
    type LocalTransform = Transform
    type EyeTransform = Transform


centered_projection = OrthoProjection(Rect(-400, -300, 800, 600))
three_quart_projection = OrthoProjection(Rect(-200, -150, 800, 600))
zero_vector = Vector3(0, 0, 0)
zero_transform = Transform()


class MockCamera:

    def __new__(cls, *args, **kwds) -> CameraBase:
        return cast(CameraBase, super().__new__(cls))

    def __init__(self, projection: Projection) -> None:
        self.projection = projection
        self.transform: TransformComponent = TransformComponent(self)
        self.zoom_level: ZoomLevel = 1
        CameraService.add_camera(cast(CameraBase, self))


class TestCameraService(unittest.TestCase):

    def test_local_to_ndc(self):
        test_params: dict[
            str, tuple[OrthoProjection, LocalCoords, NDCCoords, ZoomLevel]
        ] = {
            "Centered projection, center coords": (
                centered_projection,
                zero_vector,
                zero_vector,
                1,
            ),
            "Centered projection, corner coords": (
                centered_projection,
                Vector3(-400, -300, 1),
                Vector3(-1, -1, 1),
                1,
            ),
            "3/4 projection, local 0 coords": (
                three_quart_projection,
                zero_vector,
                Vector3(-0.5, -0.5, 0),
                1,
            ),
            "3/4 projection, center coords": (
                three_quart_projection,
                Vector3(200, 150, 0),
                zero_vector,
                1,
            ),
            "3/4 projection, corner coords": (
                three_quart_projection,
                Vector3(-200, -150, 0),
                Vector3(-1, -1, 0),
                1,
            ),
            "Centered projection, center coords, zoom level 2": (
                centered_projection,
                zero_vector,
                zero_vector,
                2,
            ),
            "Centered projection, corner coords, zoom level 2": (
                centered_projection,
                Vector3(-200, -150, 1),
                Vector3(-1, -1, 1),
                2,
            ),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                projection, local_position, expected, zoom_level = params
                test_cam = MockCamera(projection)
                test_cam.zoom_level = zoom_level
                ndc_coords = CameraService.local_to_ndc(test_cam, local_position)
                self.assertEqual(ndc_coords, expected)

    def test_ndc_to_local(self):
        test_params: dict[
            str, tuple[OrthoProjection, NDCCoords, LocalCoords, ZoomLevel]
        ] = {
            "Centered projection, center coords": (
                centered_projection,
                zero_vector,
                zero_vector,
                1,
            ),
            "Centered projection, corner coords": (
                centered_projection,
                Vector3(-1, -1, 1),
                Vector3(-400, -300, 1),
                1,
            ),
            "3/4 projection, local 0 coords": (
                three_quart_projection,
                Vector3(-0.5, -0.5, 0),
                zero_vector,
                1,
            ),
            "3/4 projection, center coords": (
                three_quart_projection,
                zero_vector,
                Vector3(200, 150, 0),
                1,
            ),
            "3/4 projection, corner coords": (
                three_quart_projection,
                Vector3(-1, -1, 0),
                Vector3(-200, -150, 0),
                1,
            ),
            "Centered projection, center coords, zoom level 2": (
                centered_projection,
                zero_vector,
                zero_vector,
                2,
            ),
            "Centered projection, corner coords, zoom level 2": (
                centered_projection,
                Vector3(-1, -1, 1),
                Vector3(-200, -150, 1),
                2,
            ),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                projection, ndc_coords, expected, zoom_level = params
                test_cam = MockCamera(projection)
                test_cam.zoom_level = zoom_level
                local_position = CameraService.ndc_to_local(test_cam, ndc_coords)
                self.assertEqual(local_position, expected)

    def test_to_local(self):
        shifted_pos_transform = Transform((10, 0))
        shifted_post_rot_transform = Transform((10, 0), 90)

        test_params: dict[
            str, tuple[WorldTransform, WorldTransform, LocalTransform]
        ] = {
            "Both default transform": (zero_transform, zero_transform, zero_transform),
            "Default camera, Different test position": (
                zero_transform,
                shifted_pos_transform,
                shifted_pos_transform,
            ),
            "Default camera, Different test position, rotation": (
                zero_transform,
                shifted_post_rot_transform,
                shifted_post_rot_transform,
            ),
            "Shifted camera, Default test position": (
                shifted_pos_transform,
                zero_transform,
                Transform((-10, 0)),
            ),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                camera_transform, world_transform, expected = params

                test_cam = MockCamera(centered_projection)
                test_cam.transform.world_position = camera_transform.position
                test_cam.transform.world_rotation = camera_transform.rotation
                test_cam.transform.world_scale = camera_transform.scale

                local_transform = CameraService.to_local(test_cam, world_transform)

                self.assertEqual(local_transform, expected)

    def test_to_eye(self):

        test_params: dict[
            str, tuple[Projection, LocalTransform, EyeTransform, ZoomLevel]
        ] = {
            "3/4 projection, local 0 coords": (
                three_quart_projection,
                zero_transform,
                Transform((200, 150)),
                1,
            ),
            "3/4 projection, counter local coords": (
                three_quart_projection,
                Transform((-200, -150)),
                zero_transform,
                1,
            ),
            "Centered projection, off center camera, origin test transform": (
                centered_projection,
                zero_transform,
                zero_transform,
                1,
            ),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                projection, local_transform, expected, zoom_level = params

                test_cam = MockCamera(projection)
                test_cam.zoom_level = zoom_level

                eye_transform = CameraService.to_eye(test_cam, local_transform)

                self.assertEqual(eye_transform, expected)

    def test_to_world(self):
        shifted_pos_transform = Transform((10, 0))
        shifted_post_rot_transform = Transform((10, 0), 90)

        test_params: dict[
            str, tuple[Projection, WorldTransform, LocalTransform, WorldTransform]
        ] = {
            "Centered projection, both default transform": (
                centered_projection,
                zero_transform,
                zero_transform,
                zero_transform,
            ),
            "Centered Projection, Different test position": (
                centered_projection,
                zero_transform,
                shifted_pos_transform,
                shifted_pos_transform,
            ),
            "Centered Projection, Different test position, rotation": (
                centered_projection,
                zero_transform,
                shifted_post_rot_transform,
                shifted_post_rot_transform,
            ),
            "3/4 projection, local 0 coords": (
                three_quart_projection,
                zero_transform,
                zero_transform,
                Transform((-200, -150)),
            ),
            "3/4 projection, counter local coords": (
                three_quart_projection,
                zero_transform,
                Transform((200, 150)),
                zero_transform,
            ),
            "Centered projection, off center camera, origin test transform": (
                centered_projection,
                Transform((100, 100)),
                zero_transform,
                Transform((100, 100)),
            ),
            "Centered projection, off center rotated camera, origin test transform": (
                centered_projection,
                Transform((100, 100), 90),
                zero_transform,
                Transform((100, 100), 90),
            ),
        }

        for index, (case, params) in enumerate(test_params.items()):
            with self.subTest(case, i=index):
                projection, cam_transform, local_transform, expected = params
                test_cam = MockCamera(projection)
                test_cam.transform.world_position = cam_transform.position
                test_cam.transform.world_rotation = cam_transform.rotation

                world_transform = CameraService.to_world(test_cam, local_transform)

                self.assertEqual(world_transform, expected)


if __name__ == "__main__":

    unittest.main()
