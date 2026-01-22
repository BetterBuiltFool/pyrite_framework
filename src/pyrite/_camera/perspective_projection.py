from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Rect

import glm

from pyrite._types.projection import Projection
from pyrite._camera.frustum import Frustum

if TYPE_CHECKING:
    pass


DEFAULT_Z_NEAR = -1
DEFAULT_Z_DEPTH = 2


class PerspectiveProjection(Projection):
    """
    Camera projection allowing for perspective in 3 dimensions.
    """

    def __init__(
        self, fov_y: float, aspect: float, z_near: float, z_far: float
    ) -> None:
        super().__init__()
        self.volume: Frustum = Frustum(fov_y, aspect, z_near, z_far)

    @property
    def far_plane(self) -> Rect:
        height = self.volume.z_far - self.volume.z_near
        angle = self.volume.fov_y / 2

        base = glm.tan(angle) * height * 2

        return Rect(0, 0, base * self.volume.aspect_ratio, base)

    @property
    def z_near(self) -> float:
        return self.volume.z_near

    @z_near.setter
    def z_near(self, z_near: float):
        self.volume.z_near = z_near

    @property
    def z_far(self) -> float:
        return self.volume.z_far

    @z_far.setter
    def z_far(self, z_far: float):
        self.volume.z_far = z_far

    @property
    def z_depth(self) -> float:
        return self.volume.z_far - self.volume.z_near

    @property
    def center_z(self) -> float:
        return self.volume.z_near + (self.z_depth / 2)

    def __repr__(self) -> str:
        return f"<PerspectiveProjection {self.volume}>"

    def __eq__(self, value: object) -> bool:
        return isinstance(value, PerspectiveProjection) and value.volume == self.volume

    def get_matrix(self) -> glm.mat4x4:
        volume = self.volume
        return glm.perspectiveLH(
            volume.fov_y,
            volume.aspect_ratio,
            volume.z_near,
            volume.z_far,
        )

    def zoom(self, zoom_factor: float) -> PerspectiveProjection:

        return PerspectiveProjection(
            self.volume.fov_y / zoom_factor,
            self.volume.aspect_ratio,
            self.volume.z_near,
            self.volume.z_far,
        )
