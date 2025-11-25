from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Rect, Vector2

from pyrite.cuboid import Cuboid
from pyrite._types.projection import Projection
from pyrite._transform.transform import Transform

if TYPE_CHECKING:
    # from pygame.typing import RectLike
    from pyrite._types.protocols import TransformLike
    from pyrite.types import CubeLike


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
            cuboid = (projection_rect, -1, 2)
        self.projection_data = Cuboid(cuboid)

    # def __init__(
    #     self,
    #     projection_rect: RectLike | None = None,
    #     z_near: float = -1,
    #     z_far: float = 1,
    # ) -> None:
    #     if projection_rect is None:
    #         # Default projection is the size of the screen
    #         display = pygame.display.get_surface()
    #         assert display is not None
    #         projection_rect = Rect(left_top=(0, 0), width_height=display.size)
    #         projection_rect.center = (0, 0)
    #     self.projection_data = Cuboid((projection_rect, (z_near, z_far - z_near)))

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

    def local_to_eye(self, local_coords: TransformLike) -> Transform:
        return Transform(local_coords.position)

    def eye_to_local(self, eye_coords: TransformLike) -> Transform:
        return Transform(eye_coords.position)

    def ndc_to_eye(self, ndc_coords: TransformLike) -> Transform:
        rect = self.projection_data.face_xy
        center = Vector2(rect.center)
        ndc_position = ndc_coords.position
        x_scaled = ndc_position.x * (rect.width / 2)
        y_scaled = ndc_position.y * (rect.height / 2)
        return Transform((x_scaled + center.x, y_scaled - center.y))

    def eye_to_ndc(self, eye_coords: TransformLike) -> Transform:
        rect = self.projection_data.face_xy
        center = Vector2(rect.center)
        eye_position = eye_coords.position
        offset = (eye_position.x - center.x, eye_position.y + center.y)
        return Transform((offset[0] / (rect.width / 2), offset[1] / (rect.height / 2)))

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
