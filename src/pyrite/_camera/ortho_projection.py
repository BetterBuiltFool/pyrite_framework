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
        self.volume = Cuboid(cuboid)

    @property
    def far_plane(self) -> Rect:
        return self.volume.face_xy

    @property
    def z_near(self) -> float:
        return self.volume.front

    @z_near.setter
    def z_near(self, z_near: float):
        self.volume.front = z_near

    @property
    def z_far(self) -> float:
        return self.volume.back

    @z_far.setter
    def z_far(self, z_far: float):
        self.volume.back = z_far

    @property
    def z_depth(self) -> float:
        return self.volume.depth

    @property
    def center_z(self) -> float:
        return self.volume.centerz

    def __repr__(self) -> str:
        return f"<OrthoProjection {self.volume}>"

    def __eq__(self, value: object) -> bool:
        return isinstance(value, OrthoProjection) and value.volume == self.volume

    def get_matrix(self) -> glm.mat4x4:
        volume = self.volume

        bottom = volume.bottom
        top = volume.top
        # Invert y, since world coords are y-up but Cuboid is y-down
        bottom = bottom - volume.height
        top = top + volume.height

        projection = glm.orthoLH(
            volume.left,
            volume.right,
            bottom,
            top,
            volume.front,
            volume.back,
        )

        # Inverting breaks the expectation of the projection orientation due to the
        # coordinate system mismatch, but adding the height breaks everything but cases
        # where the top = 0.
        # However, centery is deviation from y=0, so by doubling that and shifting by
        # it, we can cancel out the y change from inversion.
        return glm.translate(projection, glm.vec3(0, 2 * volume.centery, 0))

    def zoom(self, zoom_factor: float) -> OrthoProjection:
        rect_center = self.volume.center
        new_rect = Rect(
            0,
            0,
            self.volume.width / zoom_factor,
            self.volume.height / zoom_factor,
        )
        new_rect.center = rect_center[0] / zoom_factor, rect_center[1] / zoom_factor
        return OrthoProjection((new_rect, self.volume.front, self.volume.depth))
