from __future__ import annotations

import typing

import pygame
from pygame import FRect, Rect

if typing.TYPE_CHECKING:
    from pygame.typing import Point, RectLike


class Viewport:
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
            size = (bottomright[0] - topleft[0], topleft[1] - bottomright[1])
            frect = FRect(topleft[0], topleft[1], size[0], size[1])
        self.frect = FRect(frect)

    @staticmethod
    def NDC_to_screen(point: Point) -> Point:
        """
        Converts a point in NDC space to screen space on the current display.

        :param point: A point in NDC space
        :return: A point in pygame screen space.
        """
        display = pygame.display.get_surface()
        display_rect = display.get_rect()
        surface_width, surface_height = display_rect.size
        center_x, center_y = display_rect.center
        return (
            center_x - int(point[0] * (-surface_width / 2)),
            center_y - int(point[1] * (surface_height / 2)),
        )

    @staticmethod
    def screen_to_NDC(point: Point) -> Point:
        """
        Converts a point in screen space on the current display to NDC space.

        :param point: A point in pygame screen space.
        :return: A point in NDC space
        """
        display = pygame.display.get_surface()
        display_rect = display.get_rect()
        surface_width, surface_height = display_rect.size
        center_x, center_y = display_rect.center
        return (
            (point[0] + center_x) / (-surface_width / 2),
            (point[1] + center_y) / (surface_height / 2),
        )

    def get_display_rect(self) -> Rect:
        """
        Calculates the subrect for the sector, from the display.

        :return: A rectangle proportionate to both the surface rectangle, and the
        screen sectors' frect.
        """
        topleft = self.NDC_to_screen(self.frect.topleft)
        bottomright = self.NDC_to_screen(self.frect.bottomright)
        size = (bottomright[0] - topleft[0], topleft[1] - bottomright[1])
        return Rect(topleft[0], topleft[1], size[0], size[1])
