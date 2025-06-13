from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from ..camera.camera_service import CameraService
from ..types import Renderer

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.typing import Point
    from ..camera import Camera
    from ..types.render_target import RenderTarget


class CameraRenderer(Renderer):
    """
    A Renderer responsible for rendering camera views to screen.
    """

    _smooth: bool = False

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
