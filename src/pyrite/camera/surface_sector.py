from __future__ import annotations

import typing

import pygame
from pygame import FRect, Rect

if typing.TYPE_CHECKING:
    from pygame.typing import RectLike
    from pygame import Surface


class SurfaceSector:
    """
    Represents a portion of a surface, primarily for rendering out cameras.
    """

    def __init__(self, frect: FRect | RectLike = None, **kwds) -> None:
        """
        Represents a portion of a surface, primarily for rendering out cameras.
        Uses Normalized Device Coordinates (NDC), so
        left = -1, right = 1, top = 1, bottom = -1

        :param frect: An FRect representing the screen sector in NDC space.
        """
        if frect is None:
            if not (topleft := kwds.get("topleft")):
                topleft = (-1, 1)
            if not (bottomright := kwds.get("bottomright")):
                bottomright = (1, -1)
            frect = FRect()
            frect.topleft = topleft
            size = (bottomright[0] - topleft[0], topleft[1] - bottomright[1])
            frect.size = size
        self.frect = FRect(frect)

    def get_display_rect(self) -> Rect:
        """
        Calculates the subrect for the sector, from the display.

        :return: A rectangle proportionate to both the surface rectangle, and the
        screen sectors' frect.
        """
        return self.get_rect(pygame.display.get_surface())

    def get_rect(self, surface: Surface) -> Rect:
        """
        Calculates the subrect for the sector

        :param surface: A surface being partitioned by the screen sector
        :return: A rectangle proportionate to both the surface rectangle, and the
        screen sectors' frect.
        """
        frect = self.frect
        surface_rect = surface.get_rect()
        surface_width, surface_height = surface_rect.size
        center_x, center_y = surface_rect.center
        topleft = (
            center_x - int(frect.left * (-surface_width / 2)),
            center_y - int(frect.top * (surface_height / 2)),
        )
        size = (
            int(frect.width * (surface_width / 2)),
            int(frect.height * (surface_height / 2)),
        )
        rect = Rect()
        rect.topleft, rect.size = topleft, size
        return rect
