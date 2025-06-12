from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Rect

from ..camera.camera_service import CameraService
from ..types import Renderer

if TYPE_CHECKING:
    from collections.abc import Sequence
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
    ) -> Rect:
        """
        Draws a line to the screen, using the coordinates (in world space),
        transformed to screen space.

        :param camera: The camera whose view is being considered
        :param viewport: The viewport being drawn in.
        :param color: A color-like value to give to the line
        :param start_pos: Start position of the line in world sapce
        :param end_pos: End position of the line in world space
        :param width: The width of the line, in pixels, defaults to 1
        :return: A Rect that covers the area between the resulting line in screen space.
        """
        display = viewport.get_target_surface()

        screen_start = CameraService.world_to_screen(start_pos, camera, viewport)
        screen_end = CameraService.world_to_screen(end_pos, camera, viewport)

        return pygame.draw.line(display, color, screen_start, screen_end, width)

    @classmethod
    def draw_rect(
        cls,
        camera: Camera,
        viewport: Viewport,
        color: ColorLike,
        rect: Rect,
        width: int = 0,
        border_radius: int = -1,
        border_top_left_radius: int = -1,
        border_top_right_radius: int = -1,
        border_bottom_left_radius: int = -1,
        border_bottom_right_radius: int = -1,
    ) -> Rect:
        display = viewport.get_target_surface()

        # Remember that display is inverted compared to world
        screen_topleft = CameraService.world_to_screen(
            rect.bottomleft, camera, viewport
        )
        screen_bottomright = CameraService.world_to_screen(
            rect.topright, camera, viewport
        )

        rect_width = screen_bottomright[0] - screen_topleft[0]
        rect_height = screen_bottomright[1] - screen_topleft[1]
        draw_rect = Rect(*screen_topleft, rect_width, rect_height)

        return pygame.draw.rect(
            display,
            color,
            draw_rect,
            width,
            border_radius,
            border_top_left_radius,
            border_top_right_radius,
            border_bottom_left_radius,
            border_bottom_right_radius,
        )

    @classmethod
    def draw_polygon(
        cls,
        camera: Camera,
        viewport: Viewport,
        color: ColorLike,
        points: Sequence[Point],
        width: int = 0,
    ) -> Rect:
        display = viewport.get_target_surface()

        screen_points = [
            CameraService.world_to_screen(point, camera, viewport) for point in points
        ]

        return pygame.draw.polygon(display, color, screen_points, width)

    @classmethod
    def draw_circle(
        cls,
        camera: Camera,
        viewport: Viewport,
        color: ColorLike,
        center: Point,
        radius: int,
        width: int = 0,
        draw_top_right: bool = False,
        draw_top_left: bool = False,
        draw_bottom_left: bool = False,
        draw_bottom_right: bool = False,
    ) -> Rect:
        display = viewport.get_target_surface()

        screen_center = CameraService.world_to_screen(center, camera, viewport)

        return pygame.draw.circle(
            display,
            color,
            screen_center,
            radius,
            width,
            draw_top_right,
            draw_top_left,
            draw_bottom_left,
            draw_bottom_right,
        )

    @classmethod
    def draw_aacircle(
        cls,
        camera: Camera,
        viewport: Viewport,
        color: ColorLike,
        center: Point,
        radius: int,
        width: int = 0,
        draw_top_right: bool = False,
        draw_top_left: bool = False,
        draw_bottom_left: bool = False,
        draw_bottom_right: bool = False,
    ) -> Rect:
        display = viewport.get_target_surface()

        screen_center = CameraService.world_to_screen(center, camera, viewport)

        return pygame.draw.aacircle(
            display,
            color,
            screen_center,
            radius,
            width,
            draw_top_right,
            draw_top_left,
            draw_bottom_left,
            draw_bottom_right,
        )

    @classmethod
    def draw_ellipse(
        cls,
        camera: Camera,
        viewport: Viewport,
        color: ColorLike,
        rect: Rect,
        width: int = 0,
    ) -> Rect:
        display = viewport.get_target_surface()

        # Remember that display is inverted compared to world
        screen_topleft = CameraService.world_to_screen(
            rect.bottomleft, camera, viewport
        )
        screen_bottomright = CameraService.world_to_screen(
            rect.topright, camera, viewport
        )

        rect_width = screen_bottomright[0] - screen_topleft[0]
        rect_height = screen_bottomright[1] - screen_topleft[1]
        draw_rect = Rect(*screen_topleft, rect_width, rect_height)

        return pygame.draw.ellipse(
            display,
            color,
            draw_rect,
            width,
        )

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
