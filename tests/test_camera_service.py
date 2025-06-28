from __future__ import annotations
import pathlib
import sys
from typing import TYPE_CHECKING
import unittest

from pygame import Rect, Vector3

if TYPE_CHECKING:
    from typing import TypeAlias

    LocalCoords: TypeAlias = Vector3
    NDCCoords: TypeAlias = Vector3
    ZoomLevel: TypeAlias = float


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.services import CameraService  # noqa:E402
from src.pyrite.rendering import OrthoProjection  # noqa: E402
from src.pyrite.types.projection import Projection  # noqa:E402
from src.pyrite.transform import TransformComponent, Transform  # noqa: E402


centered_projection = OrthoProjection(Rect(-400, -300, 800, 600))
three_quart_projection = OrthoProjection(Rect(-200, -150, 800, 600))
zero_vector = Vector3(0, 0, 0)


class MockCamera:

    def __init__(self, projection: Projection) -> None:
        self.projection = projection
        self.transform: TransformComponent = TransformComponent(self)
        self.zoom_level: ZoomLevel = 1
        CameraService.add_camera(self)


class TestCameraService(unittest.TestCase):

    def local_to_ndc(
        self,
        projection: OrthoProjection,
        local_position: LocalCoords,
        expected: NDCCoords,
        zoom_level: ZoomLevel = 1,
    ):
        test_cam = MockCamera(projection)
        test_cam.zoom_level = zoom_level
        ndc_coords = CameraService.local_to_ndc(test_cam, local_position)
        self.assertEqual(ndc_coords, expected)

    def test_local_to_ndc(self):
        test_params: list[tuple[OrthoProjection, LocalCoords, NDCCoords, ZoomLevel]] = [
            # Centered projection, center coords
            (centered_projection, zero_vector, zero_vector, 1),
            # Centered projection, corner coords
            (centered_projection, Vector3(-400, -300, 1), Vector3(-1, -1, 1), 1),
            # 3/4 projection, local 0 coords
            (three_quart_projection, zero_vector, Vector3(-0.5, -0.5, 0), 1),
            # 3/4 projection, center coords
            (three_quart_projection, Vector3(200, 150, 0), zero_vector, 1),
            # 3/4 projection, corner coords
            (three_quart_projection, Vector3(-200, -150, 0), Vector3(-1, -1, 0), 1),
            # Centered projection, center coords, zoom level 2
            (centered_projection, zero_vector, zero_vector, 2),
            # Centered projection, corner coords, zoom level 2
            (centered_projection, Vector3(-200, -150, 1), Vector3(-1, -1, 1), 2),
        ]

        for params in test_params:
            self.local_to_ndc(*params)

    def ndc_to_local(
        self,
        projection: OrthoProjection,
        ndc_coords: NDCCoords,
        expected: LocalCoords,
        zoom_level: ZoomLevel = 1,
    ):
        test_cam = MockCamera(projection)
        test_cam.zoom_level = zoom_level
        local_position = CameraService.ndc_to_local(test_cam, ndc_coords)
        self.assertEqual(local_position, expected)

    def test_ndc_to_local(self):
        test_params: list[tuple[OrthoProjection, NDCCoords, LocalCoords, ZoomLevel]] = [
            # Centered projection, center coords
            (centered_projection, zero_vector, zero_vector, 1),
            # Centered projection, corner coords
            (centered_projection, Vector3(-1, -1, 1), Vector3(-400, -300, 1), 1),
            # 3/4 projection, local 0 coords
            (three_quart_projection, Vector3(-0.5, -0.5, 0), zero_vector, 1),
            # 3/4 projection, center coords
            (three_quart_projection, zero_vector, Vector3(200, 150, 0), 1),
            # 3/4 projection, corner coords
            (three_quart_projection, Vector3(-1, -1, 0), Vector3(-200, -150, 0), 1),
            # Centered projection, center coords, zoom level 2
            (centered_projection, zero_vector, zero_vector, 2),
            # Centered projection, corner coords, zoom level 2
            (centered_projection, Vector3(-1, -1, 1), Vector3(-200, -150, 1), 2),
        ]

        for params in test_params:
            self.ndc_to_local(*params)

    def test_to_local(self):
        # Centered projection, both default transform
        projection = OrthoProjection(Rect(-400, -300, 800, 600))
        test_cam = MockCamera(projection)

        world_transform = Transform((0, 0), 0, (0, 0))

        local_transform = CameraService.to_local(test_cam, world_transform)

        expected = Transform((0, 0), 0, (0, 0))

        self.assertEqual(local_transform, expected)

        # Centered Projection, Default camera, Different test position,

        world_transform = Transform((10, 0), 0, (0, 0))

        local_transform = CameraService.to_local(test_cam, world_transform)

        expected = Transform((10, 0), 0, (0, 0))

        self.assertEqual(local_transform, expected)

        # Centered Projection, Default camera, Different test position, rotation,

        world_transform = Transform((10, 0), 90, (0, 0))

        local_transform = CameraService.to_local(test_cam, world_transform)

        expected = Transform((10, 0), 90, (0, 0))

        self.assertEqual(local_transform, expected)

    def test_to_eye(self):

        projection = OrthoProjection(Rect(-200, -150, 800, 600))

        assert projection.far_plane.center == (200, 150)

        # 3/4 projection, local 0 coords
        test_cam = MockCamera(projection)

        local_transform = Transform((0, 0), 0, (0, 0))

        eye_transform = CameraService.to_eye(test_cam, local_transform)

        expected = Transform((200, 150), 0, (0, 0))

        self.assertEqual(eye_transform, expected)

        # 3/4 projection, counter local coords

        local_transform = Transform((-200, -150), 0, (0, 0))

        eye_transform = CameraService.to_eye(test_cam, local_transform)

        expected = Transform((0, 0), 0, (0, 0))

        self.assertEqual(eye_transform, expected)

        # Centered projection, off center camera, origin test transform
        projection = OrthoProjection(Rect(-400, -300, 800, 600))

        assert projection.far_plane.center == (0, 0)
        test_cam.projection = projection

        local_transform = Transform((0, 0), 0, (0, 0))

        eye_transform = CameraService.to_eye(test_cam, local_transform)

        expected = Transform((0, 0), 0, (0, 0))

        self.assertEqual(eye_transform, expected)

    def test_to_world(self):
        # Centered projection, both default transform
        projection = OrthoProjection(Rect(-400, -300, 800, 600))
        test_cam = MockCamera(projection)

        local_transform = Transform((0, 0), 0, (0, 0))

        world_transform = CameraService.to_world(test_cam, local_transform)

        expected = Transform((0, 0), 0, (0, 0))

        self.assertEqual(world_transform, expected)

        # Centered Projection, Default camera, Different test position,

        local_transform = Transform((10, 0), 0, (0, 0))

        world_transform = CameraService.to_world(test_cam, local_transform)

        expected = Transform((10, 0), 0, (0, 0))

        self.assertEqual(world_transform, expected)

        # Centered Projection, Default camera, Different test position, rotation,

        local_transform = Transform((10, 0), 90, (0, 0))

        world_transform = CameraService.to_world(test_cam, local_transform)

        expected = Transform((10, 0), 90, (0, 0))

        self.assertEqual(world_transform, expected)

        # 3/4 projection, local 0 coords

        projection = OrthoProjection(Rect(-200, -150, 800, 600))

        assert projection.far_plane.center == (200, 150)
        test_cam.projection = projection

        local_transform = Transform((0, 0), 0, (0, 0))

        world_transform = CameraService.to_world(test_cam, local_transform)

        expected = Transform((-200, -150), 0, (0, 0))

        self.assertEqual(world_transform, expected)

        # 3/4 projection, counter local coords

        local_transform = Transform((200, 150), 0, (0, 0))

        world_transform = CameraService.to_world(test_cam, local_transform)

        expected = Transform((0, 0), 0, (0, 0))

        self.assertEqual(world_transform, expected)

        # Centered projection, off center camera, origin test transform
        projection = OrthoProjection(Rect(-400, -300, 800, 600))

        assert projection.far_plane.center == (0, 0)
        test_cam.projection = projection

        test_cam.transform.world_position = (100, 100)

        local_transform = Transform((0, 0), 0, (0, 0))

        world_transform = CameraService.to_world(test_cam, local_transform)

        expected = Transform((100, 100), 0, (0, 0))

        self.assertEqual(world_transform, expected)

        # Centered projection, off center rotated camera, origin test transform

        test_cam.transform.world_position = (100, 0)
        test_cam.transform.world_rotation = 90

        local_transform = Transform((0, 0), 0, (0, 0))

        world_transform = CameraService.to_world(test_cam, local_transform)

        expected = Transform((100, 0), 90, (0, 0))

        self.assertEqual(world_transform, expected)


if __name__ == "__main__":

    unittest.main()
