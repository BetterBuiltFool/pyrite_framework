from __future__ import annotations

import typing

import pygame

if typing.TYPE_CHECKING:
    from pygame.typing import RectLike


class SurfaceSector:
    """
    Represents a portion of a surface, primarily for rendering out cameras.
    """

    def __init__(self, frect: pygame.FRect | RectLike = (0, 0, 1, 1)) -> None:
        """
        Represents a portion of a surface, primarily for rendering out cameras.

        :param frect: A float rect representing the portion of a surface the sector
        takes up. Values should be between 0 and 1. Defaults to (0, 0, 1, 1),
        full surface.
        """
        self.frect = pygame.FRect(frect)

    def get_display_rect(self) -> pygame.Rect:
        """
        Calculates the subrect for the sector, from the display.

        :return: A rectangle proportionate to both the surface rectangle, and the
        screen sectors' frect.
        """
        return self.get_rect(pygame.display.get_surface())

    def get_rect(self, surface: pygame.Surface) -> pygame.Rect:
        """
        Calculates the subrect for the sector

        :param surface: A surface being partitioned by the screen sector
        :return: A rectangle proportionate to both the surface rectangle, and the
        screen sectors' frect.
        """
        frect = self.frect
        surface_width, surface_height = surface.get_rect().size
        topleft = (
            int(frect.left * surface_width),
            int(frect.top * surface_height),
        )
        size = (
            int(frect.width * surface_width),
            int(frect.height * surface_height),
        )
        rect = pygame.Rect()
        rect.topleft, rect.size = topleft, size
        return rect
