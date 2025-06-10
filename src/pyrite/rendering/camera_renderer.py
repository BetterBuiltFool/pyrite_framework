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
        # Convert start_pos, end_pos to local coords
        start_pos = CameraService.point_to_local(camera, start_pos)
        end_pos = CameraService.point_to_local(camera, end_pos)
        # Convert local coords to ndc coords
        ndc_start = CameraService.local_to_ndc(camera, Vector3(*start_pos, 0))
        ndc_end = CameraService.local_to_ndc(camera, Vector3(*end_pos, 0))
        # Convert ndc_coords to screen coords
        screen_start = viewport.ndc_to_screen(ndc_start)
        screen_end = viewport.ndc_to_screen(ndc_end)
        # And draw to screen
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

        topleft = CameraService.point_to_local(camera, rect.topleft)
        bottomright = CameraService.point_to_local(camera, rect.bottomright)

        ndc_tl = CameraService.local_to_ndc(camera, Vector3(*topleft, 0))
        ndc_br = CameraService.local_to_ndc(camera, Vector3(*bottomright, 0))

        screen_tl = viewport.ndc_to_screen(ndc_tl)
        screen_br = viewport.ndc_to_screen(ndc_br)

        rect_width = screen_tl[0] + screen_br[0]
        rect_height = screen_tl[1] + screen_br[1]
        draw_rect = Rect(*screen_tl, rect_width, rect_height)

        pygame.draw.rect(display, color, draw_rect, width)

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
