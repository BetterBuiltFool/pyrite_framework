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
        Uses Normalized Device Coordinates (ndc), so
        left = -1, right = 1, top = 1, bottom = -1

        :param frect: An FRect representing the screen viewport in ndc space.
        """
        if frect is None:
            if not (topleft := kwds.get("topleft")):
                topleft = (-1, 1)
            if not (bottomright := kwds.get("bottomright")):
                bottomright = (1, -1)
            size = (bottomright[0] - topleft[0], topleft[1] - bottomright[1])
            frect = FRect(topleft[0], topleft[1], size[0], size[1])
        self.frect = FRect(frect)

    def ndc_to_screen(self, ndc_coord: Point) -> Point:
        """
        Converts a point in ndc space to screen coordinates on the current display.

        :param point: A point in ndc space
        :return: A point in pygame screen coordinates.
        """

        display_rect = self.get_display_rect()
        surface_width, surface_height = display_rect.size
        center_x, center_y = display_rect.center
        view_point = (
            center_x - int(ndc_coord[0] * (-surface_width / 2)),
            center_y - int(ndc_coord[1] * (surface_height / 2)),
        )
        return view_point

    def screen_to_ndc(self, screen_point: Point) -> Point:
        """
        Converts a point in screen space on the current display to ndc space.

        :param screen_point: A point in pygame screen space.
        :return: A point in ndc space
        """
        display_rect = self.get_display_rect()
        surface_width, surface_height = display_rect.size
        center_x, center_y = display_rect.center
        ndc_point = (
            (screen_point[0] - center_x) / (surface_width / 2),
            (screen_point[1] - center_y) / (-surface_height / 2),
        )
        return ndc_point

    def get_display_rect(self) -> Rect:
        """
        Calculates the subrect for the viewport, from the display.

        :return: A rectangle proportionate to both the surface rectangle, and the
        screen viewports' frect.
        """
        return self._get_subrect(self.frect, pygame.display.get_surface().size)

    # TODO Consider @functools.cache?
    @staticmethod
    def _get_subrect(frect: FRect, size: Point) -> Rect:
        center_x, center_y = size[0] / 2, size[1] / 2
        left = center_x - (frect.left * -center_x)
        top = center_y - (frect.top * center_y)
        width = frect.width * center_x
        height = frect.height * center_y
        return Rect(left, top, width, height)
