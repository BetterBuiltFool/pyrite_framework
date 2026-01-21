from __future__ import annotations

from typing import Any, TYPE_CHECKING

import glm
import pygame
from pygame import FRect, Rect

from pyrite._transform.transform import Transform

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.typing import Point, RectLike


class Viewport:
    """
    Represents a portion of a surface, primarily for rendering out cameras.
    """

    _viewports: dict[Any, Viewport] = {}

    DEFAULT: Viewport

    def __init__(self, relative_rect: FRect | RectLike) -> None:
        self._relative_rect = FRect(relative_rect)

    @property
    def relative_rect(self) -> FRect:
        """
        An FRect representing the viewport in relative terms.
        Uses relative coordinates to display center, so
        left = -1, right = 1, top = 1, bottom = -1, full width = 2, full height = 2
        """
        return self._relative_rect

    @relative_rect.setter
    def relative_rect(self, relative_rect: FRect):
        self._relative_rect = relative_rect
        display_surf = pygame.display.get_surface()
        assert display_surf is not None
        self._update_display_rect(display_surf.size)

    @property
    def display_rect(self) -> Rect:
        """
        A Rect representing the actual pixel space of the viewport, relative to the top
        left corner of the screen. Follows pygame standard, `display.topleft == (0,0)`.
        """
        return self._display_rect

    @property
    def matrix(self) -> glm.mat4x4:
        """
        A matrix for converting clip coordinates into screen coordinates. Uses the
        display_rect.
        """
        display_rect = self.display_rect

        left = display_rect.left
        right = display_rect.right
        bottom = display_rect.bottom
        top = display_rect.top

        matrix = glm.orthoLH(
            left,
            right,
            bottom,
            top,
            -1,
            1,
        )
        matrix = glm.inverse(matrix)
        return matrix

    @classmethod
    def add_new_viewport(
        cls, label: Any, relative_rect: FRect | RectLike | None = None, **kwds
    ) -> Viewport:
        """
        Adds a new viewport to the viewport dict.

        :param label: An object to be associated with the new Viewport.
        :param relative_rect: An FRect representing the screen viewport in ndc space.
            Uses Normalized Device Coordinates (ndc), so
            left = -1, right = 1, top = 1, bottom = -1
        :return: The created viewport.
        """
        if relative_rect is None:
            if not (topleft := kwds.get("topleft")):
                topleft = (-1, 1)
            if not (bottomright := kwds.get("bottomright")):
                bottomright = (1, -1)
            size = (bottomright[0] - topleft[0], topleft[1] - bottomright[1])
            relative_rect = FRect(topleft[0], topleft[1], size[0], size[1])
        viewport = Viewport(relative_rect)
        return cls.add_viewport(label, viewport)

    @classmethod
    def add_viewport(cls, label: Any, viewport: Viewport) -> Viewport:
        """
        Adds a new viewport to the viewport dict.

        :param label: An object to be associated with the new Viewport.
        :param viewport: An existing viewport object to be added.
        :return: The existing viewport object.
        """
        cls._viewports[label] = viewport
        return viewport

    def clip_to_viewport(self, clip_coords: Transform) -> Transform:
        """
        Converts a point in clip space to viewport space.

        :param clip_coords: A Transform value in clip space.
        :return: The equivalent transform in viewport space.
        """

        return Transform.from_matrix(self.matrix * clip_coords.matrix)

    def viewport_to_clip(self, screen_point: Point) -> Transform:
        """
        Converts a point in viewport space to clip space.

        :param screen_point: A point in viewport space.
        :return: A Transform representing clip space coordinates.
        """
        display_rect = self._display_rect
        surface_width, surface_height = display_rect.size
        center_x, center_y = display_rect.center
        ndc_point = (
            (screen_point[0] - center_x) / (surface_width / 2),
            (screen_point[1] - center_y) / (-surface_height / 2),
        )
        return Transform.from_2d(ndc_point)

    def get_display_rect(self) -> Rect:
        """
        Calculates the subrect for the viewport, from the display.

        :return: A rectangle proportionate to both the surface rectangle, and the
        screen viewports' relative_rect.
        """
        return self._display_rect

    def get_target_surface(self) -> Surface:
        """
        Gets the target surface for the viewport. This will always be the current
        display.
        """
        surface = pygame.display.get_surface()
        assert surface is not None
        return surface

    def get_target_rect(self) -> Rect:
        """
        Gets the target rect representing the subrect of the display.
        """
        return self._display_rect

    def _update_display_rect(self, size: Point):
        abs_rect = self._get_subrect(self.relative_rect, size)
        self._display_rect = abs_rect

    @classmethod
    def update_viewports(cls, size: Point):
        """
        Updates all of the contained viewports so their absolute size is appropriate
        for the passed size.

        :param size: A point describing the size of the display.
        """
        for viewport in cls._viewports.values():
            viewport._update_display_rect(size)
        cls.DEFAULT._update_display_rect(size)

    @staticmethod
    def _get_subrect(relative_rect: FRect, size: Point) -> Rect:
        center_x, center_y = size[0] / 2, size[1] / 2
        left = center_x - (relative_rect.left * -center_x)
        top = center_y - (relative_rect.top * center_y)
        width = relative_rect.width * center_x
        height = relative_rect.height * center_y
        return Rect(left, top, width, height)


# Set the default Viewport, since we can't form an instance inside that class's
# declaration.
Viewport.DEFAULT = Viewport((-1, 1, 2, 2))
# Do NOT set the display rect yet, since the display might not exist yet.
