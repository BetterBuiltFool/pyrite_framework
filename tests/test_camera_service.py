from __future__ import annotations
import pathlib
import sys
import unittest

from pygame import Rect, Vector3


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.camera.camera_service import CameraService  # noqa:E402
from src.pyrite.rendering.ortho_projection import OrthProjection  # noqa: E402
from src.pyrite.types.projection import Projection  # noqa:E402
from src.pyrite.transform import TransformComponent  # noqa: E402


class MockCamera:

    def __init__(self, projection: Projection) -> None:
        self.projection = projection
        self.transform = TransformComponent(self)
        self.zoom_level = 1
        CameraService.add_camera(self)


class TestCameraService(unittest.TestCase):

    def test_local_to_ndc(self):
        projection = OrthProjection(Rect(-400, -300, 800, 600))
        test_cam = MockCamera(projection)

        local_position = Vector3(0, 0, 0)

        ndc_coords = CameraService.local_to_ndc(test_cam, local_position)

        expected = Vector3(0, 0, 0)

        self.assertEqual(ndc_coords, expected)


if __name__ == "__main__":

    unittest.main()
