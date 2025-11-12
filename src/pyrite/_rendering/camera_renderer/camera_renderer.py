from __future__ import annotations

from abc import abstractmethod
from typing import cast, TYPE_CHECKING

import pygame

from pyrite._services.camera_service import CameraServiceProvider as CameraService
from pyrite._services.camera_service import DefaultCameraService
from pyrite._types.camera import Camera
from pyrite._types.renderer import Renderer
from pyrite._types.protocols import RenderTarget

if TYPE_CHECKING:
    pass


class CameraRenderer(Renderer[Camera, RenderTarget]):

    @property
    @abstractmethod
    def smooth_scale(self) -> bool: ...

    @smooth_scale.setter
    def smooth_scale(self, smooth_scale: bool): ...


class DefaultCameraRenderer(CameraRenderer):

    def __init__(self) -> None:
        self._smooth: bool = False
        self.scale_method = pygame.transform.scale

    @property
    def smooth_scale(self) -> bool:
        return self._smooth

    @smooth_scale.setter
    def smooth_scale(self, smooth_scale: bool):
        self._smooth = smooth_scale
        if smooth_scale:
            self.scale_method = pygame.transform.smoothscale
        else:
            self.scale_method = pygame.transform.scale

    def render(self, renderable: Camera, target: RenderTarget):
        surface = target.get_target_surface()
        render_rect = target.get_target_rect()
        camera_service = cast(
            DefaultCameraService,
            CameraService._service,
        )
        camera_view = camera_service._surfaces[renderable]
        # if not target.crop:
        #     # Not cropping, so scale the view instead.
        camera_view = self.scale_method(camera_view, render_rect.size)

        crop_rect = render_rect.copy()
        crop_rect.center = camera_view.get_rect().center
        surface.blit(
            camera_view,
            render_rect.topleft,
            crop_rect,
        )
