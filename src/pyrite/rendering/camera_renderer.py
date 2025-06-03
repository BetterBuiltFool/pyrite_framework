from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from ..camera.camera_service import CameraService
from ..types import Renderer

if TYPE_CHECKING:
    from .viewport import Viewport
    from ..camera import Camera


class CameraRenderer(Renderer):

    @classmethod
    def render(cls, camera: Camera, viewport: Viewport):
        window = pygame.display.get_surface()
        render_rect = viewport.get_display_rect()
        window.blit(
            camera.scale_view(CameraService._surfaces.get(camera), render_rect.size),
            render_rect.topleft,
        )
