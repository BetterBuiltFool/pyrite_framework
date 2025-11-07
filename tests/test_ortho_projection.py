from __future__ import annotations

import unittest
from typing import TYPE_CHECKING

from pygame import Rect, Vector2, Vector3

from pyrite._camera.ortho_projection import OrthoProjection

if TYPE_CHECKING:
    type LocalCoords = Vector2
    type EyeCoords = Vector3
    type NDCCoords = Vector3
    type ZoomLevel = float

CENTERED_100_SQUARE = OrthoProjection((-50, -50, 100, 100))
CORNER_100_SQUARE = OrthoProjection((0, 0, 100, 100))
CENTERED_200X100 = OrthoProjection((-100, -50, 200, 100))

CENTERED_800X600 = OrthoProjection(Rect(-400, -300, 800, 600))
THREE_QUART_800X600 = OrthoProjection(Rect(-200, -150, 800, 600))

ZERO_POINT = Vector2(0)
ZERO_3D = Vector3(0)


class TestOrthoProjection(unittest.TestCase):

    def test_ndc_to_eye(self) -> None:

        params: dict[str, tuple[OrthoProjection, Vector3, Vector3]] = {
            "Base Case C100S": (
                CENTERED_100_SQUARE,
                Vector3(0, 0, 0),
                Vector3(0, 0, 0),
            ),
            "Top left corner C100S": (
                CENTERED_100_SQUARE,
                Vector3(-1, 1, 0),
                Vector3(-50, 50, 0),
            ),
            "Bottom Right corner C100S": (
                CENTERED_100_SQUARE,
                Vector3(1, -1, 0),
                Vector3(50, -50, 0),
            ),
            "3/4x 3/4y C100S": (
                CENTERED_100_SQUARE,
                Vector3(0.5, 0.5, 0),
                Vector3(25, 25, 0),
            ),
            "Base Case Cr100S": (
                CORNER_100_SQUARE,
                Vector3(0, 0, 0),
                Vector3(50, -50, 0),
            ),
            "Top left corner Cr100S": (
                CORNER_100_SQUARE,
                Vector3(-1, 1, 0),
                Vector3(0, 0, 0),
            ),
            "Bottom Right corner Cr100S": (
                CORNER_100_SQUARE,
                Vector3(1, -1, 0),
                Vector3(100, -100, 0),
            ),
            "3/4x 3/4y Cr100S": (
                CORNER_100_SQUARE,
                Vector3(0.5, 0.5, 0),
                Vector3(75, -25, 0),
            ),
            "Base Case C2x1": (CENTERED_200X100, Vector3(0, 0, 0), Vector3(0, 0, 0)),
            "Top left corner C2x1": (
                CENTERED_200X100,
                Vector3(-1, 1, 0),
                Vector3(-100, 50, 0),
            ),
            "Bottom Right corner C2x1": (
                CENTERED_200X100,
                Vector3(1, -1, 0),
                Vector3(100, -50, 0),
            ),
            "3/4x 3/4y C2x1": (
                CENTERED_200X100,
                Vector3(0.5, 0.5, 0),
                Vector3(50, 25, 0),
            ),
        }

        for case, (projection, ndc_coords, expected_coords) in params.items():
            with self.subTest(i=case):
                result = projection.ndc_to_eye(ndc_coords)

                self.assertEqual(result, expected_coords)

    def test_eye_to_ndc(self) -> None:

        params: dict[str, tuple[OrthoProjection, Vector3, Vector3]] = {
            "Base Case C100S": (
                CENTERED_100_SQUARE,
                Vector3(0, 0, 0),
                Vector3(0, 0, 0),
            ),
            "Top left corner C100S": (
                CENTERED_100_SQUARE,
                Vector3(-50, 50, 0),
                Vector3(-1, 1, 0),
            ),
            "Bottom Right corner C100S": (
                CENTERED_100_SQUARE,
                Vector3(50, -50, 0),
                Vector3(1, -1, 0),
            ),
            "3/4x 3/4y C100S": (
                CENTERED_100_SQUARE,
                Vector3(25, 25, 0),
                Vector3(0.5, 0.5, 0),
            ),
            "Base Case Cr100S": (
                CORNER_100_SQUARE,
                Vector3(50, -50, 0),
                Vector3(0, 0, 0),
            ),
            "Top left corner Cr100S": (
                CORNER_100_SQUARE,
                Vector3(0, 0, 0),
                Vector3(-1, 1, 0),
            ),
            "Bottom Right corner Cr100S": (
                CORNER_100_SQUARE,
                Vector3(100, -100, 0),
                Vector3(1, -1, 0),
            ),
            "3/4x 3/4y Cr100S": (
                CORNER_100_SQUARE,
                Vector3(75, -25, 0),
                Vector3(0.5, 0.5, 0),
            ),
            "Base Case C2x1": (CENTERED_200X100, Vector3(0, 0, 0), Vector3(0, 0, 0)),
            "Top left corner C2x1": (
                CENTERED_200X100,
                Vector3(-100, 50, 0),
                Vector3(-1, 1, 0),
            ),
            "Bottom Right corner C2x1": (
                CENTERED_200X100,
                Vector3(100, -50, 0),
                Vector3(1, -1, 0),
            ),
            "3/4x 3/4y C2x1": (
                CENTERED_200X100,
                Vector3(50, 25, 0),
                Vector3(0.5, 0.5, 0),
            ),
        }

        for case, (projection, eye_coords, expected_coords) in params.items():
            with self.subTest(i=case):
                result = projection.eye_to_ndc(eye_coords)

                self.assertEqual(result, expected_coords)

    def test_local_to_eye(self) -> None:
        test_params: dict[
            str, tuple[OrthoProjection, LocalCoords, EyeCoords, ZoomLevel]
        ] = {
            "3/4 projection, local 0 coords": (
                THREE_QUART_800X600,
                ZERO_POINT,
                ZERO_3D,
                1,
            ),
            "3/4 projection, center coords": (
                THREE_QUART_800X600,
                Vector2(-200, -150),
                Vector3(-200, -150, 0),
                1,
            ),
            "Centered projection, off center camera, origin test transform": (
                CENTERED_800X600,
                ZERO_POINT,
                ZERO_3D,
                1,
            ),
        }

        for case, (projection, local_coords, expected, zoom) in test_params.items():
            with self.subTest(i=case):
                eye_coords = projection.local_to_eye(local_coords, zoom)

                self.assertEqual(eye_coords, expected)

    def test_eye_to_local(self) -> None:
        test_params: dict[
            str, tuple[OrthoProjection, LocalCoords, EyeCoords, ZoomLevel]
        ] = {
            "3/4 projection, local 0 coords": (
                THREE_QUART_800X600,
                ZERO_POINT,
                ZERO_3D,
                1,
            ),
            "3/4 projection, center coords": (
                THREE_QUART_800X600,
                Vector2(-200, -150),
                Vector3(-200, -150, 0),
                1,
            ),
            "Centered projection, off center camera, origin test transform": (
                CENTERED_800X600,
                ZERO_POINT,
                ZERO_3D,
                1,
            ),
        }

        for case, (projection, expected, eye_coords, zoom) in test_params.items():
            with self.subTest(i=case):
                local_coords = projection.eye_to_local(eye_coords, zoom)

                self.assertEqual(local_coords, expected)

    def test_zoom(self) -> None:

        test_params: dict[str, tuple[OrthoProjection, ZoomLevel, OrthoProjection]] = {
            "Centered, zoom level 2": (
                CENTERED_100_SQUARE,
                2,
                OrthoProjection((-25, -25, 50, 50)),
            ),
            "Corner, zoom level 2": (
                CORNER_100_SQUARE,
                2,
                OrthoProjection((25, 25, 50, 50)),
            ),
            "Centered 200x100, zoom level 2": (
                CENTERED_200X100,
                2,
                OrthoProjection((-50, -25, 100, 50)),
            ),
        }

        for case, (projection, zoom_level, expected) in test_params.items():
            with self.subTest(i=case):
                zoom_proj = projection.zoom(zoom_level)

                self.assertEqual(zoom_proj, expected)


if __name__ == "__main__":
    unittest.main()
