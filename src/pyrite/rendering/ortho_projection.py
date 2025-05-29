from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Vector3

from ..types.projection import Projection

if TYPE_CHECKING:
    from pygame import Rect
    from pygame.typing import Point


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

    def screen_to_NDC(self, screen_point: Point, viewport: Rect) -> Point:
        # Viewport may be smaller or larger than the projection, so adjust.
        width_ratio = self.projection_rect.width / viewport.width
        height_ratio = self.projection_rect.height / viewport.height

        # Convert screen space to projection space.
        point = (
            (screen_point[0] * width_ratio) - (self.projection_rect.width / 2),
            (screen_point[1] * height_ratio) - (self.projection_rect.height / 2),
        )
        # Normalize coordinates
        ndc_point = (
            point[0] / (self.projection_rect.width / 2),
            -point[1] / (self.projection_rect.height / 2),
            self.z_far,
        )
        return Vector3(*ndc_point)

    def view_to_NDC(self, view_position: Vector3) -> Vector3:
        width = self.projection_rect.width
        height = self.projection_rect.height
        depth = self.z_far - self.z_near
        projected_point = (
            view_position.x - width / 2,
            view_position.y - height / 2,
            view_position.z - depth / 2,
        )
        ndc_point = (
            projected_point[0] / (width / 2),
            projected_point[1] / (height / 2),
            projected_point[2] / (depth / 2),
        )
        return Vector3(*ndc_point)
