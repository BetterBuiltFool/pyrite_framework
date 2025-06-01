from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

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
        self._z_near = z_near
        self._z_far = z_far

    @property
    def far_plane(self) -> Rect:
        return self.projection_rect

    @property
    def z_near(self) -> float:
        return self._z_near

    @z_near.setter
    def z_near(self, distance: float):
        self._z_near = distance

    @property
    def z_far(self) -> float:
        return self._z_far

    @z_far.setter
    def z_far(self, distance: float):
        self._z_far = distance

    @property
    def z_depth(self) -> float:
        return self._z_far - self._z_near
