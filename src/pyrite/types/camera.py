from __future__ import annotations

from abc import ABC
from collections.abc import Iterable
from typing import TYPE_CHECKING

from src.pyrite.types.renderable import Renderable
from src.pyrite.types.enums import Layer, RenderLayers

import pygame
from pygame import Vector2

if TYPE_CHECKING:
    from src.pyrite.types import Container


class CameraBase(ABC):
    """
    Defines the important attributes of a camera for the sake of drawing onto its
    surface.

    Can be constructed from the window.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        layer_mask: tuple[Layer] = None,
    ) -> None:
        self.surface = surface
        if layer_mask is None:
            layer_mask = ()
        self.layer_mask = layer_mask

    def clear(self):
        """
        Overwrite the surface to allow new drawing on top.
        Default fill is solid black.
        """
        self.surface.fill((0, 0, 0, 0))

    def draw(self, renderable: pygame.Surface, rect: pygame.Rect):
        """
        Draws a surface onto the camera's surface, adjusting the rectangle position to
        local space.

        :param renderable: Surface being drawn onto the camera surface
        :param rect: Rectangle conveying world space position of the renderable.
        """
        self.surface.blit(
            renderable,
            self.to_local(rect.topleft),
        )

    def cull(self, items: Iterable[Renderable]) -> Iterable[Renderable]:
        """
        Removes any renderables that do not fall within view of the camera.

        :param items: Any iterable containing the renderable to be culled.
        :return: A generator containing only renderables in view of the camera's
        viewport.
        """
        return (item for item in items if self._in_view(item.get_rect()))

    def _in_view(self, rect: pygame.Rect) -> bool:
        return self.surface.get_rect().colliderect(rect)

    def to_local(self, point: pygame.typing.Point) -> Vector2:
        """
        Converts a point in world space to local space.

        :param point: A point, in world space
        :return: The local space equivalent of _point_
        """
        return Vector2(point)

    def to_world(self, point: pygame.typing.Point) -> Vector2:
        """
        Converts a point in local space to world space.

        :param point: A point, in local space
        :return: The world space equivalent of _point_
        """

        return Vector2(point)


class Camera(CameraBase, Renderable):
    """
    Basic form of a camera that is capable of rendering to the screen.
    """

    def __init__(
        self,
        max_size: pygame.typing.Point,
        position: pygame.typing.Point = None,
        layer_mask: tuple[Layer] = None,
        container: Container = None,
        enabled=True,
        draw_index: int = 0,
    ) -> None:
        """
        Basic form of a camera that is capable of rendering to the screen.

        :param max_size: Largest, most zoomed out size of the camera.
        :param position: Position of the center of the camera surface, defaults to None
        None will give the center of the viewport.
        :param layer_mask: Layers that the camera will exclude from rendering,
        defaults to None
        :param container: The instance of the game to which the rengerable belongs,
        defaults to None. See Renderable.
        :param enabled: Whether the Renderable will be drawn to the screen,
        defaults to True
        :param draw_index: Index determining draw order within a layer, defaults to 0
        """
        self.max_size = Vector2(max_size)
        surface = pygame.Surface(self.max_size)
        self.viewport = surface.get_rect()
        """
        A rectangle representing the actual viewable area of the camera
        """
        if position is None:
            position = self.viewport.center
        self.position = Vector2(position)
        CameraBase.__init__(self, surface=surface, layer_mask=layer_mask)
        Renderable.__init__(
            self,
            container=container,
            enabled=enabled,
            layer=RenderLayers.CAMERA,
            draw_index=draw_index,
        )

    def clear(self):
        """
        Overwrite the surface to allow new drawing on top.
        Basic camera fills with transparent black.
        """
        self.surface.fill((0, 0, 0, 255))

    def _in_view(self, rect: pygame.Rect) -> bool:
        return self.get_rect().colliderect(rect)

    def get_surface_rect(self) -> pygame.Rect:
        """
        Gets the rect of the camera's surface, in worldspace, centered on the position.

        :return: A Rectangle matching the size of the camera surface, in worldspace.
        """
        return self.surface.get_rect(center=self.position)

    def get_rect(self) -> pygame.Rect:
        """
        Gives the viewport converted to worldspace.

        :return: A Rectangle matching the size of the viewport, with worldspace
        coordinates.
        """
        return pygame.Rect(
            self.to_world(self.viewport.topleft),
            self.viewport.size,
        )

    def render(self, delta_time: float) -> tuple[pygame.Surface, pygame.typing.Point]:
        return (
            self.surface.subsurface(self.viewport),
            (0, 0),
        )

    def to_local(self, point: pygame.typing.Point) -> Vector2:
        point = Vector2(point)

        return point - Vector2(self.get_surface_rect().topleft)

    def to_world(self, point: pygame.typing.Point) -> Vector2:
        point = Vector2(point)

        return point + Vector2(self.get_surface_rect().topleft)

    def zoom(self, zoom_level: float):
        """
        Adjusts the viewport size to match the zoom level.
        Viewport size is scaled in terms of max_size/zoom_level,
        so overall size is 1/zoom_level^2.
        (i.e. zoom_level 2 means half width and half height, 1/4 overall size)

        If the viewport is off center, and the new zoom size would push the viewport
        out of bounds, the viewport is adjusted to fit in the surface. Full zoom out
        will center the viewport.

        :param zoom_level: Integer value indicating zoom level
        :raises ValueError: Raised if zoom level is greater than one
        """
        if zoom_level < 1:
            raise ValueError("Cannot zoom out beyond zoom_level 1")

        center = self.viewport.center

        # Race condition (possibly?) means we can't assign to viewport directly without
        # a potential crash from pushing viewport out of bounds
        # So, we create a new rect to calculate with and assign it to viewport later.
        # This ensures a valid subsurface can always be taken from viewport
        new_view = pygame.Rect(self.viewport)
        new_view.size = self.max_size / zoom_level
        new_view.center = center

        top = new_view.top
        left = new_view.left

        # Clamp viewport to stay in bounds
        new_view.top = max(0, min(top, new_view.height + top))
        new_view.left = max(0, min(left, new_view.width + left))

        # Overwrite the viewport with the new (valid) rect
        self.viewport = new_view
