from __future__ import annotations

from typing import TYPE_CHECKING

from ..camera.camera_service import CameraService
from ..types import Renderer

if TYPE_CHECKING:
    from ..camera import Camera
    from ..types.render_target import RenderTarget


class CameraRenderer(Renderer):

    @classmethod
    def render(cls, camera: Camera, render_target: RenderTarget):
        surface = render_target.get_target_surface()
        render_rect = render_target.get_target_rect()
        camera_view = CameraService._surfaces.get(camera)
        if not render_target.crop:
            # Not cropping, so scale the view instead.
            camera_view = CameraService._scale_view(camera, render_rect.size)

        crop_rect = render_rect.copy()
        crop_rect.center = camera_view.get_rect().center
        surface.blit(
            camera_view,
            render_rect.topleft,
            crop_rect,
        )
