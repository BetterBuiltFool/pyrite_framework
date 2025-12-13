from __future__ import annotations

import unittest
from typing import TYPE_CHECKING

from pygame import Vector2, Vector3

from pyrite._camera.ortho_projection import (
    OrthoProjection,
    DEFAULT_Z_NEAR,
    DEFAULT_Z_DEPTH,
)
from pyrite._transform.transform import Transform

if TYPE_CHECKING:
    type LocalCoords = Vector2
    type EyeCoords = Vector2
    type NDCCoords = Vector3
    type ZoomLevel = float

CENTERED_100_SQUARE = OrthoProjection(
    ((-50, -50, 100, 100), DEFAULT_Z_NEAR, DEFAULT_Z_DEPTH),
)
CORNER_100_SQUARE = OrthoProjection(
    ((0, 0, 100, 100), DEFAULT_Z_NEAR, DEFAULT_Z_DEPTH),
)
CENTERED_200X100 = OrthoProjection(
    ((-100, -50, 200, 100), DEFAULT_Z_NEAR, DEFAULT_Z_DEPTH),
)

CENTERED_800X600 = OrthoProjection(
    ((-400, -300, 800, 600), DEFAULT_Z_NEAR, DEFAULT_Z_DEPTH),
)
THREE_QUART_800X600 = OrthoProjection(
    ((-200, -150, 800, 600), DEFAULT_Z_NEAR, DEFAULT_Z_DEPTH),
)

ZERO_POINT = Vector2(0)
ZERO_3D = Vector3(0)


class TestOrthoProjection(unittest.TestCase):

    def test_ndc_to_eye(self) -> None:

        params: dict[str, tuple[OrthoProjection, Vector2, Vector2]] = {
            "Base Case C100S": (
                CENTERED_100_SQUARE,
                Vector2(0, 0),
                Vector2(0, 0),
            ),
            "Top left corner C100S": (
                CENTERED_100_SQUARE,
                Vector2(-1, 1),
                Vector2(-50, 50),
            ),
            "Bottom Right corner C100S": (
                CENTERED_100_SQUARE,
                Vector2(1, -1),
                Vector2(50, -50),
            ),
            "3/4x 3/4y C100S": (
                CENTERED_100_SQUARE,
                Vector2(0.5, 0.5),
                Vector2(25, 25),
            ),
            "Base Case Cr100S": (
                CORNER_100_SQUARE,
                Vector2(0, 0),
                Vector2(50, -50),
            ),
            "Top left corner Cr100S": (
                CORNER_100_SQUARE,
                Vector2(-1, 1),
                Vector2(0, 0),
            ),
            "Bottom Right corner Cr100S": (
                CORNER_100_SQUARE,
                Vector2(1, -1),
                Vector2(100, -100),
            ),
            "3/4x 3/4y Cr100S": (
                CORNER_100_SQUARE,
                Vector2(0.5, 0.5),
                Vector2(75, -25),
            ),
            "Base Case C2x1": (
                CENTERED_200X100,
                Vector2(0, 0),
                Vector2(0, 0),
            ),
            "Top left corner C2x1": (
                CENTERED_200X100,
                Vector2(-1, 1),
                Vector2(-100, 50),
            ),
            "Bottom Right corner C2x1": (
                CENTERED_200X100,
                Vector2(1, -1),
                Vector2(100, -50),
            ),
            "3/4x 3/4y C2x1": (
                CENTERED_200X100,
                Vector2(0.5, 0.5),
                Vector2(50, 25),
            ),
        }

        for case, (projection, ndc_coords, expected_coords) in params.items():
            with self.subTest(i=case):
                result = projection.ndc_to_eye(Transform.from_2d(ndc_coords))

                self.assertEqual(result.position, expected_coords)

    def test_eye_to_ndc(self) -> None:

        params: dict[str, tuple[OrthoProjection, Vector2, Vector2]] = {
            "Base Case C100S": (
                CENTERED_100_SQUARE,
                Vector2(0, 0),
                Vector2(0, 0),
            ),
            "Top left corner C100S": (
                CENTERED_100_SQUARE,
                Vector2(-50, 50),
                Vector2(-1, 1),
            ),
            "Bottom Right corner C100S": (
                CENTERED_100_SQUARE,
                Vector2(50, -50),
                Vector2(1, -1),
            ),
            "3/4x 3/4y C100S": (
                CENTERED_100_SQUARE,
                Vector2(25, 25),
                Vector2(0.5, 0.5),
            ),
            "Base Case Cr100S": (
                CORNER_100_SQUARE,
                Vector2(50, -50),
                Vector2(0, 0),
            ),
            "Top left corner Cr100S": (
                CORNER_100_SQUARE,
                Vector2(0, 0),
                Vector2(-1, 1),
            ),
            "Bottom Right corner Cr100S": (
                CORNER_100_SQUARE,
                Vector2(100, -100),
                Vector2(1, -1),
            ),
            "3/4x 3/4y Cr100S": (
                CORNER_100_SQUARE,
                Vector2(75, -25),
                Vector2(0.5, 0.5),
            ),
            "Base Case C2x1": (
                CENTERED_200X100,
                Vector2(0, 0),
                Vector2(0, 0),
            ),
            "Top left corner C2x1": (
                CENTERED_200X100,
                Vector2(-100, 50),
                Vector2(-1, 1),
            ),
            "Bottom Right corner C2x1": (
                CENTERED_200X100,
                Vector2(100, -50),
                Vector2(1, -1),
            ),
            "3/4x 3/4y C2x1": (
                CENTERED_200X100,
                Vector2(50, 25),
                Vector2(0.5, 0.5),
            ),
        }

        for case, (projection, eye_coords, expected_coords) in params.items():
            with self.subTest(i=case):
                result = projection.eye_to_ndc(Transform.from_2d(eye_coords.xy))

                self.assertEqual(result.position, expected_coords)

    def test_local_to_eye(self) -> None:
        test_params: dict[str, tuple[OrthoProjection, LocalCoords, EyeCoords]] = {
            "3/4 projection, local 0 coords": (
                THREE_QUART_800X600,
                ZERO_POINT,
                ZERO_POINT,
            ),
            "3/4 projection, center coords": (
                THREE_QUART_800X600,
                Vector2(-200, -150),
                Vector2(-200, -150),
            ),
            "Centered projection, off center camera, origin test transform": (
                CENTERED_800X600,
                ZERO_POINT,
                ZERO_POINT,
            ),
        }

        for case, (projection, local_coords, expected) in test_params.items():
            with self.subTest(i=case):
                eye_coords = projection.local_to_eye(Transform.from_2d(local_coords))

                self.assertEqual(eye_coords.position, expected)

    def test_eye_to_local(self) -> None:
        test_params: dict[str, tuple[OrthoProjection, LocalCoords, EyeCoords]] = {
            "3/4 projection, local 0 coords": (
                THREE_QUART_800X600,
                ZERO_POINT,
                ZERO_POINT,
            ),
            "3/4 projection, center coords": (
                THREE_QUART_800X600,
                Vector2(-200, -150),
                Vector2(-200, -150),
            ),
            "Centered projection, off center camera, origin test transform": (
                CENTERED_800X600,
                ZERO_POINT,
                ZERO_POINT,
            ),
        }

        for case, (projection, expected, eye_coords) in test_params.items():
            with self.subTest(i=case):
                local_coords = projection.eye_to_local(Transform.from_2d(eye_coords))

                self.assertEqual(local_coords.position, expected)

    def test_zoom(self) -> None:

        test_params: dict[str, tuple[OrthoProjection, ZoomLevel, OrthoProjection]] = {
            "Centered, zoom level 2": (
                CENTERED_100_SQUARE,
                2,
                OrthoProjection((-25, -25, -1, 50, 50, 2)),
            ),
            "Corner, zoom level 2": (
                CORNER_100_SQUARE,
                2,
                OrthoProjection((0, 0, -1, 50, 50, 2)),
            ),
            "Centered 200x100, zoom level 2": (
                CENTERED_200X100,
                2,
                OrthoProjection((-50, -25, -1, 100, 50, 2)),
            ),
        }

        for case, (projection, zoom_level, expected) in test_params.items():
            with self.subTest(i=case):
                zoom_proj = projection.zoom(zoom_level)

                self.assertEqual(zoom_proj, expected)


if __name__ == "__main__":
    unittest.main()
