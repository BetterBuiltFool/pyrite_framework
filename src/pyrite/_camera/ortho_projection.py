from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Rect

import glm

from pyrite.cuboid import Cuboid
from pyrite._types.projection import Projection

if TYPE_CHECKING:
    from pyrite.types import CubeLike


DEFAULT_Z_NEAR = -1
DEFAULT_Z_DEPTH = 2


class OrthoProjection(Projection):
    """
    An orthographic projection data object, useful for 2D applications.

    Height and width are in pixels. (0, 0) in the projection will be local (0, 0) for
    the assigned camera.

    Follows pygame Rect rules, so +y = down.
    """

    def __init__(self, cuboid: CubeLike | None) -> None:
        if cuboid is None:
            display = pygame.display.get_surface()
            assert display is not None
            projection_rect = Rect(left_top=(0, 0), width_height=display.size)
            projection_rect.center = (0, 0)
            cuboid = (projection_rect, DEFAULT_Z_NEAR, DEFAULT_Z_DEPTH)
        self.projection_data = Cuboid(cuboid)

    @property
    def far_plane(self) -> Rect:
        return self.projection_data.face_xy

    @property
    def z_near(self) -> float:
        return self.projection_data.front

    @z_near.setter
    def z_near(self, z_near: float):
        self.projection_data.front = z_near

    @property
    def z_far(self) -> float:
        return self.projection_data.back

    @z_far.setter
    def z_far(self, z_far: float):
        self.projection_data.back = z_far

    @property
    def z_depth(self) -> float:
        return self.projection_data.depth

    @property
    def center_z(self) -> float:
        return self.projection_data.centerz

    def __repr__(self) -> str:
        return f"<OrthoProjection {self.projection_data}>"

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, OrthoProjection)
            and value.projection_data == self.projection_data
        )

    def get_matrix(self) -> glm.mat4x4:
        proj_data = self.projection_data

        bottom = proj_data.bottom
        top = proj_data.top
        # Invert y, since world coords are y-up but Cuboid is y-down
        bottom = bottom - proj_data.height
        top = top + proj_data.height

        projection = glm.orthoLH(
            proj_data.left,
            proj_data.right,
            bottom,
            top,
            proj_data.front,
            proj_data.back,
        )

        # Inverting breaks the expectation of the projection orientation due to the
        # coordinate system mismatch, but adding the height breaks everything but cases
        # where the top = 0.
        # However, centery is deviation from y=0, so by doubling that and shifting by
        # it, we can cancel out the y change from inversion.
        return glm.translate(projection, glm.vec3(0, 2 * proj_data.centery, 0))

    def zoom(self, zoom_factor: float) -> OrthoProjection:
        rect_center = self.projection_data.center
        new_rect = Rect(
            0,
            0,
            self.projection_data.width / zoom_factor,
            self.projection_data.height / zoom_factor,
        )
        new_rect.center = rect_center[0] / zoom_factor, rect_center[1] / zoom_factor
        return OrthoProjection(
            (new_rect, self.projection_data.front, self.projection_data.depth)
        )
