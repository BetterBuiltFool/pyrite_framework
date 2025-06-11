from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Rect, Vector3

from ..camera.camera_service import CameraService
from ..types import Renderer

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.typing import ColorLike, Point
    from ..camera import Camera
    from .viewport import Viewport
    from ..types.render_target import RenderTarget


class CameraRenderer(Renderer):
    _smooth: bool = False

    @classmethod
    def draw_line(
        cls,
        camera: Camera,
        viewport: Viewport,
        color: ColorLike,
        start_pos: Point,
        end_pos: Point,
        width: int = 1,
    ):
        """
        Draws a line to the screen, using the coordinates (in world space),
        transformed to screen space.

        :param camera: The camera whose view is being considered
        :param viewport: The viewport being drawn in.
        :param color: A color-like value to give to the line
        :param start_pos: Start position of the line in world sapce
        :param end_pos: End position of the line in world space
        :param width: The width of the line, in pixels, defaults to 1
        """
        display = viewport.get_target_surface()

        screen_start = cls._world_to_screen(start_pos, camera, viewport)
        screen_end = cls._world_to_screen(end_pos, camera, viewport)

        pygame.draw.line(display, color, screen_start, screen_end, width)

    @classmethod
    def draw_rect(
        cls,
        camera: Camera,
        viewport: Viewport,
        color: ColorLike,
        rect: Rect,
        width: int = 1,
        # Add other params eventually
    ):
        display = viewport.get_target_surface()

        # Remember that display is inverted compared to world
        screen_topleft = cls._world_to_screen(rect.bottomleft, camera, viewport)
        screen_bottomright = cls._world_to_screen(rect.topright, camera, viewport)

        rect_width = screen_bottomright[0] - screen_topleft[0]
        rect_height = screen_bottomright[1] - screen_topleft[1]
        draw_rect = Rect(*screen_topleft, rect_width, rect_height)

        pygame.draw.rect(display, color, draw_rect, width)

    @classmethod
    def _world_to_screen(
        cls, point: Point, camera: Camera, viewport: Viewport
    ) -> Point:
        local_coords = CameraService.point_to_local(camera, point)
        if viewport.crop:
            coords = viewport.local_to_screen(local_coords)
        else:
            eye_coords = CameraService.local_point_to_projection(camera, local_coords)
            ndc_coords = CameraService.local_to_ndc(camera, Vector3(*eye_coords, 0))
            coords = viewport.ndc_to_screen(ndc_coords)
        return coords

    @classmethod
    def render(cls, delta_time: float, camera: Camera, render_target: RenderTarget):
        surface = render_target.get_target_surface()
        render_rect = render_target.get_target_rect()
        camera_view = CameraService._surfaces.get(camera)
        if not render_target.crop:
            # Not cropping, so scale the view instead.
            camera_view = cls._scale_view(camera_view, render_rect.size)

        crop_rect = render_rect.copy()
        crop_rect.center = camera_view.get_rect().center
        surface.blit(
            camera_view,
            render_rect.topleft,
            crop_rect,
        )

    @classmethod
    def set_smooth_scale(cls, smooth: bool = True):
        cls._smooth = smooth
        if smooth:
            cls._scale_view = pygame.transform.smoothscale
        else:
            cls._scale_view = pygame.transform.scale

    @classmethod
    def get_smooth_scale(cls) -> bool:
        return cls._smooth

    @classmethod
    def _scale_view(cls, surface: Surface, size: Point) -> Surface:
        """
        Scales the surface using the set scaling method.

        :param surface: The surface to be scaled
        :param size: The size the surface is being scaled to.
        :return: The scaled surface
        """
        return pygame.transform.scale(surface, size)
