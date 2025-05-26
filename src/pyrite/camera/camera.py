from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from .camera_service import CameraService
from .default_camera import DefaultCamera
from .surface_sector import SurfaceSector
from ..enum import Layer, RenderLayers
from ..rendering.camera_renderer import CameraRenderer
from ..rendering.rect_bounds import RectBounds
from ..rendering.view_plane import ViewPlane
from ..types import Renderable

import pygame
from pygame import Vector2

if TYPE_CHECKING:
    from ..types import Container, CameraBase
    from pygame.typing import Point


class Camera(DefaultCamera, Renderable):
    """
    Basic form of a camera that is capable of rendering to the screen.
    """

    def __init__(
        self,
        max_size: Point,
        position: Point = None,
        surface_sectors: SurfaceSector | Sequence[SurfaceSector] = None,
        viewport: pygame.Rect = None,
        smooth_scale: bool = False,
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
        :param surface_sectors: Defines sections of the screen to render to. If multiple
        surface sectors are used, the camera will be rendered and scaled to each of
        them.
        :param viewport: A rectangle representing the actual viewable area of the
        camera, defaults to None.
        None will give the center of the viewport.
        :param smooth_scale: Determines if the camera will be smoothed when run through
        the scaling step, defaults to False.
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
        CameraService.add_camera(self)
        if viewport is None:
            viewport = surface.get_rect()
        self.viewport = viewport
        """
        A rectangle representing the actual viewable area of the camera
        """
        self._smooth_scale = smooth_scale
        self._scale_method = (
            pygame.transform.scale if not smooth_scale else pygame.transform.smoothscale
        )
        if position is None:
            position = self.viewport.center
        self.position = Vector2(position)
        if surface_sectors is None:
            surface_sectors = [SurfaceSector()]
        if not isinstance(surface_sectors, Sequence):
            surface_sectors = [surface_sectors]
        self.surface_sectors: Sequence[SurfaceSector] = surface_sectors
        self._zoom_level: float = 1
        DefaultCamera.__init__(self, surface=surface, layer_mask=layer_mask)
        Renderable.__init__(
            self,
            container=container,
            enabled=enabled,
            layer=RenderLayers.CAMERA,
            draw_index=draw_index,
        )

    @property
    def smooth_scale(self) -> bool:
        return self._smooth_scale

    @smooth_scale.setter
    def smooth_scale(self, flag: bool):
        self._smooth_scale = flag
        if flag:
            self._scale_method = pygame.transform.smoothscale
            return
        self._scale_method = pygame.transform.scale

    def clear(self):
        """
        Overwrite the surface to allow new drawing on top.
        Basic camera fills with transparent black.
        """
        self.surface.fill((0, 0, 0, 255))

    def _in_view(self, rect: pygame.Rect) -> bool:
        return self.get_viewport_rect().colliderect(rect)

    def get_surface_rect(self) -> pygame.Rect:
        """
        Gets the rect of the camera's surface, in worldspace, centered on the position.

        :return: A Rectangle matching the size of the camera surface, in worldspace.
        """
        return self.surface.get_rect(center=self.position)

    def get_viewport_rect(self) -> pygame.Rect:
        """
        Gives the viewport converted to worldspace.

        :return: A Rectangle matching the size of the viewport, with worldspace
        coordinates.
        """
        return pygame.Rect(
            self.to_world(self.viewport.topleft),
            self.viewport.size,
        )

    def get_rect(self) -> pygame.Rect:
        return self.viewport.move_to(topleft=(0, 0))

    def get_bounds(self) -> RectBounds:
        return RectBounds(self.get_rect())

    def get_view_bounds(self) -> ViewPlane:
        # TODO Find a way of caching this per frame so we don't regenerate it for each
        # renderable.
        return ViewPlane(self.get_viewport_rect())

    def render(self, delta_time: float, camera: CameraBase):
        CameraRenderer.render(self, camera)

    def to_local(self, point: Point) -> Vector2:
        # TODO Slog through this and make it work
        # It renders correctly, but bounds end up mirrored above the sprites.
        # point = Vector2(point)

        # point -= Vector2(self.get_surface_rect().bottomleft)

        # point.y = -point.y

        # return point

        return point - Vector2(self.get_surface_rect().topleft)

    def to_world(self, point: Point) -> Vector2:
        # point = Vector2(point)

        # point += Vector2(self.get_surface_rect().bottomleft)

        # point.y = -point.y

        # return point

        return point + Vector2(self.get_surface_rect().topleft)

    def screen_to_world(self, point: Point, sector_index: int = 0) -> Vector2:
        sector = self.surface_sectors[sector_index]
        sector_rect = self._get_sector_rect(sector)

        viewport_world = self.get_viewport_rect()

        viewport_space_position = self._screen_to_viewport(
            point, sector_rect, Vector2(viewport_world.size)
        )

        return viewport_space_position.elementwise() + viewport_world.topleft

    def screen_to_world_clamped(
        self, point: Point, sector_index: int = 0
    ) -> Vector2 | None:
        sector = self.surface_sectors[sector_index]
        sector_rect = self._get_sector_rect(sector)

        if not sector_rect.collidepoint(point):
            return None

        viewport_world = self.get_viewport_rect()

        viewport_space_position = self._screen_to_viewport(
            point, sector_rect, Vector2(viewport_world.size)
        )

        return viewport_space_position.elementwise() + viewport_world.topleft

    def _screen_to_viewport(
        self, point: Point, sector_rect: pygame.Rect, viewport_size: Vector2
    ) -> Vector2:
        relative_pos = pygame.Vector2(point) - pygame.Vector2(sector_rect.topleft)
        scale_x, scale_y = (
            pygame.Vector2(sector_rect.size).elementwise() / viewport_size
        )
        viewport_space_position: pygame.Vector2 = relative_pos.elementwise() / (
            scale_x,
            scale_y,
        )
        return viewport_space_position

    def _get_sector_rect(self, sector: SurfaceSector) -> pygame.Rect:
        return sector.get_display_rect()

    def scale_view(
        self, camera_surface: pygame.Surface, target_size: Point
    ) -> pygame.Surface:
        """
        Returns a scaled version of the camera's view surface using the camera's chosen
        scale method.

        :param camera_surface: the rendered camera surface
        :param target_size: Destination size of the surface
        :return: The scaled surface.
        """
        return self._scale_method(camera_surface, target_size)

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
        self._zoom_level = zoom_level

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
