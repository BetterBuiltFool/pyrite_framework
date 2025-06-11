from __future__ import annotations
import pathlib
import sys
import unittest

from pygame import Rect, Vector3


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.camera.camera_service import CameraService  # noqa:E402
from src.pyrite.rendering.ortho_projection import OrthoProjection  # noqa: E402
from src.pyrite.types.projection import Projection  # noqa:E402
from src.pyrite.transform import TransformComponent, Transform  # noqa: E402


class MockCamera:

    def __init__(self, projection: Projection) -> None:
        self.projection = projection
        self.transform: TransformComponent = TransformComponent(self)
        self.zoom_level = 1
        CameraService.add_camera(self)


class TestCameraService(unittest.TestCase):

    def test_local_to_ndc(self):
        # Centered projection, center coords
        projection = OrthoProjection(Rect(-400, -300, 800, 600))
        test_cam = MockCamera(projection)

        local_position = Vector3(0, 0, 0)

        ndc_coords = CameraService.local_to_ndc(test_cam, local_position)

        expected = Vector3(0, 0, 0)

        self.assertEqual(ndc_coords, expected)

        # Centered projection, corner coords

        local_position = Vector3(-400, -300, 1)

        ndc_coords = CameraService.local_to_ndc(test_cam, local_position)

        expected = Vector3(-1, -1, 1)

        self.assertEqual(ndc_coords, expected)

        # 3/4 projection, local 0 coords

        projection = OrthoProjection(Rect(-200, -150, 800, 600))
        # center = (200, 150)
        assert projection.far_plane.center == (200, 150)
        test_cam.projection = projection

        local_position = Vector3(0, 0, 0)

        ndc_coords = CameraService.local_to_ndc(test_cam, local_position)

        expected = Vector3(-0.5, -0.5, 0)

        self.assertEqual(ndc_coords, expected)

        # 3/4 projection, center coords

        local_position = Vector3(200, 150, 0)

        ndc_coords = CameraService.local_to_ndc(test_cam, local_position)

        expected = Vector3(0, 0, 0)

        self.assertEqual(ndc_coords, expected)

        # 3/4 projection, corner coords

        local_position = Vector3(-200, -150, 0)

        ndc_coords = CameraService.local_to_ndc(test_cam, local_position)

        expected = Vector3(-1, -1, 0)

        self.assertEqual(ndc_coords, expected)

        # Centered projection, center coords, zoom level 2
        projection = OrthoProjection(Rect(-400, -300, 800, 600))
        test_cam.projection = projection

        test_cam.zoom_level = 2

        local_position = Vector3(0, 0, 0)

        ndc_coords = CameraService.local_to_ndc(test_cam, local_position)

        expected = Vector3(0, 0, 0)

        self.assertEqual(ndc_coords, expected)

        # Centered projection, corner coords, zoom level 2

        local_position = Vector3(-200, -150, 1)

        ndc_coords = CameraService.local_to_ndc(test_cam, local_position)

        expected = Vector3(-1, -1, 1)

        self.assertEqual(ndc_coords, expected)

    def test_ndc_to_local(self):
        # Centered projection, center coords
        projection = OrthoProjection(Rect(-400, -300, 800, 600))
        test_cam = MockCamera(projection)

        ndc_coords = Vector3(0, 0, 0)

        local_position = CameraService.ndc_to_local(test_cam, ndc_coords)

        expected = Vector3(0, 0, 0)

        self.assertEqual(local_position, expected)

        # Centered projection, corner coords

        ndc_coords = Vector3(-1, -1, 1)

        local_position = CameraService.ndc_to_local(test_cam, ndc_coords)

        expected = Vector3(-400, -300, 1)

        self.assertEqual(local_position, expected)

        # 3/4 projection, local 0 coords

        projection = OrthoProjection(Rect(-200, -150, 800, 600))
        # center = (200, 150)
        assert projection.far_plane.center == (200, 150)
        test_cam.projection = projection

        ndc_coords = Vector3(-0.5, -0.5, 0)

        local_position = CameraService.ndc_to_local(test_cam, ndc_coords)

        expected = Vector3(0, 0, 0)

        self.assertEqual(local_position, expected)

        # 3/4 projection, center coords

        ndc_coords = Vector3(0, 0, 0)

        local_position = CameraService.ndc_to_local(test_cam, ndc_coords)

        expected = Vector3(200, 150, 0)

        self.assertEqual(local_position, expected)

        # 3/4 projection, corner coords

        ndc_coords = Vector3(-1, -1, 0)

        local_position = CameraService.ndc_to_local(test_cam, ndc_coords)

        expected = Vector3(-200, -150, 0)

        self.assertEqual(local_position, expected)

        # Centered projection, center coords, zoom level 2
        projection = OrthoProjection(Rect(-400, -300, 800, 600))
        test_cam.projection = projection

        test_cam.zoom_level = 2

        ndc_coords = Vector3(0, 0, 0)

        local_position = CameraService.ndc_to_local(test_cam, ndc_coords)

        expected = Vector3(0, 0, 0)

        self.assertEqual(local_position, expected)

        # Centered projection, corner coords, zoom level 2

        ndc_coords = Vector3(-1, -1, 1)

        local_position = CameraService.ndc_to_local(test_cam, ndc_coords)

        expected = Vector3(-200, -150, 1)

        self.assertEqual(local_position, expected)

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

        # 3/4 projection, local 0 coords

        projection = OrthoProjection(Rect(-200, -150, 800, 600))

        assert projection.far_plane.center == (200, 150)
        test_cam.projection = projection

        world_transform = Transform((0, 0), 0, (0, 0))

        local_transform = CameraService.to_local(test_cam, world_transform)

        expected = Transform((200, 150), 0, (0, 0))

        self.assertEqual(local_transform, expected)

        # 3/4 projection, counter local coords

        world_transform = Transform((-200, -150), 0, (0, 0))

        local_transform = CameraService.to_local(test_cam, world_transform)

        expected = Transform((0, 0), 0, (0, 0))

        self.assertEqual(local_transform, expected)

        # Centered projection, off center camera, origin test transform
        projection = OrthoProjection(Rect(-400, -300, 800, 600))

        assert projection.far_plane.center == (0, 0)
        test_cam.projection = projection

        test_cam.transform.world_position = (100, 100)

        world_transform = Transform((0, 0), 0, (0, 0))

        local_transform = CameraService.to_local(test_cam, world_transform)

        expected = Transform((-100, -100), 0, (0, 0))

        self.assertEqual(local_transform, expected)

        # Centered projection, off center rotated camera, origin test transform

        test_cam.transform.world_position = (100, 0)
        test_cam.transform.world_rotation = 90

        world_transform = Transform((0, 0), 0, (0, 0))

        local_transform = CameraService.to_local(test_cam, world_transform)

        expected = Transform((0, -100), -90, (0, 0))

        self.assertEqual(local_transform, expected)

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
