from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Vector3

from ..types.projection import Projection

if TYPE_CHECKING:
    from pygame import Rect


class OrthProjection(Projection):

    def __init__(
        self, projection_rect: Rect = None, z_near: float = -1, z_far: float = 1
    ) -> None:
        if projection_rect is None:
            # Default projection is the size of the screen
            display = pygame.display.get_surface()
            projection_rect = Rect(left_top=(0, 0), width_height=display.size)
            projection_rect.center = (0, 0)
        self.projection_rect = projection_rect
        self.z_near = z_near
        self.z_far = z_far

    @property
    def far_plane(self) -> Rect:
        return self.projection_rect

    def clip_to_NDC(self, clip_coords: Vector3) -> Vector3:
        width = self.projection_rect.width
        height = self.projection_rect.height
        depth = self.z_far - self.z_near
        projected_point = (
            clip_coords.x - width / 2,
            clip_coords.y - height / 2,
            clip_coords.z - depth / 2,
        )
        ndc_point = (
            projected_point[0] / (width / 2),
            projected_point[1] / (height / 2),
            projected_point[2] / (depth / 2),
        )
        return Vector3(*ndc_point)

    def NDC_to_clip(self, ndc_coords: Vector3) -> Vector3:
        width = self.projection_rect.width
        height = self.projection_rect.height
        depth = self.z_far - self.z_near

        projected_point = (
            ndc_coords.x * (width / 2),
            ndc_coords.y * (height / 2),
            ndc_coords.z * (depth / 2),
        )

        clip_point = (
            projected_point[0] + (width / 2),
            projected_point[1] + (height / 2),
            projected_point[2] + (depth / 2),
        )
        return Vector3(*clip_point)
