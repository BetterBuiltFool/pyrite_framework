from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Rect, Vector2

from pyrite._types.projection import Projection
from pyrite._transform.transform import Transform

if TYPE_CHECKING:
    from pygame.typing import RectLike
    from pyrite._types.protocols import TransformLike


class OrthoProjection(Projection):
    """
    An orthographic projection data object, useful for 2D applications.

    Height and width are in pixels. (0, 0) in the projection will be local (0, 0) for
    the assigned camera.

    Follows pygame Rect rules, so +y = down.
    """

    def __init__(
        self,
        projection_rect: RectLike | None = None,
        z_near: float = -1,
        z_far: float = 1,
    ) -> None:
        if projection_rect is None:
            # Default projection is the size of the screen
            display = pygame.display.get_surface()
            assert display is not None
            projection_rect = Rect(left_top=(0, 0), width_height=display.size)
            projection_rect.center = (0, 0)
        self.projection_rect = Rect(projection_rect)
        self._z_near = z_near
        self._z_far = z_far

    @property
    def far_plane(self) -> Rect:
        return self.projection_rect

    @property
    def z_near(self) -> float:
        return self._z_near

    @z_near.setter
    def z_near(self, z_near: float):
        self._z_near = z_near

    @property
    def z_far(self) -> float:
        return self._z_far

    @z_far.setter
    def z_far(self, z_far: float):
        self._z_far = z_far

    @property
    def z_depth(self) -> float:
        return self._z_far - self._z_near

    @property
    def center_z(self) -> float:
        return self._z_far - (self.z_depth / 2)

    def __repr__(self) -> str:
        return f"<OrthoProjection {self.projection_rect}, {self.z_near}, {self.z_far}>"

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, OrthoProjection)
            and value.projection_rect == self.projection_rect
            and self.z_near == value.z_near
            and self.z_far == value.z_far
        )

    def local_to_eye(self, local_coords: TransformLike) -> Transform:
        return Transform(local_coords.position)

    def eye_to_local(self, eye_coords: TransformLike) -> Transform:
        return Transform(eye_coords.position)

    # def ndc_to_eye(self, ndc_coords: Vector3) -> Vector3:
    #     rect = self.projection_rect
    #     center = Vector3(*rect.center, self.center_z)
    #     x_scaled = ndc_coords.x * (rect.width / 2)
    #     y_scaled = ndc_coords.y * (rect.height / 2)
    #     z_scaled = ndc_coords.z * (self.z_depth / 2)
    #     return Vector3(
    #         x_scaled + center.x,
    #         y_scaled - center.y,
    #         z_scaled + center.z,
    #     )

    def ndc_to_eye(self, ndc_coords: TransformLike) -> Transform:
        rect = self.projection_rect
        center = Vector2(rect.center)
        ndc_position = ndc_coords.position
        x_scaled = ndc_position.x * (rect.width / 2)
        y_scaled = ndc_position.y * (rect.height / 2)
        return Transform((x_scaled + center.x, y_scaled - center.y))

    # def eye_to_ndc(self, eye_coords: Vector3) -> Vector3:
    #     rect = self.projection_rect
    #     center = Vector3(*rect.center, self.center_z)
    #     offset = (
    #         eye_coords.x - center.x,
    #         eye_coords.y + center.y,
    #         eye_coords.z - center.z,
    #     )
    #     return Vector3(
    #         offset[0] / (rect.width / 2),
    #         offset[1] / (rect.height / 2),
    #         offset[2] / (self.z_depth / 2),
    #     )

    def eye_to_ndc(self, eye_coords: TransformLike) -> Transform:
        rect = self.projection_rect
        center = Vector2(rect.center)
        eye_position = eye_coords.position
        offset = (eye_position.x - center.x, eye_position.y + center.y)
        return Transform((offset[0] / (rect.width / 2), offset[1] / (rect.height / 2)))

    def zoom(self, zoom_factor: float) -> OrthoProjection:
        rect_center = self.projection_rect.center
        new_rect = Rect(
            0,
            0,
            self.projection_rect.width / zoom_factor,
            self.projection_rect.height / zoom_factor,
        )
        new_rect.center = rect_center[0] / zoom_factor, rect_center[1] / zoom_factor
        return OrthoProjection(new_rect, self.z_near, self.z_far)
