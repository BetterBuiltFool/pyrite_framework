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
        if render_target.crop:
            # If we need to crop:
            subsurface_rect = render_rect.copy()
            if not (
                subsurface_rect.size[0] > camera_view.size[0]
                or subsurface_rect.size[1] > camera_view.size[1]
            ):
                # We can only crop if the target is smaller.
                # Otherwise it's an illegal operation.
                subsurface_rect.center = camera_view.get_rect().center
                # Crop from the center of the view
                camera_view = camera_view.subsurface(subsurface_rect)
        else:
            # Not cropping, so scale the view instead.
            camera_view = camera.scale_view(camera_view, render_rect.size)
        surface.blit(
            camera_view,
            render_rect.topleft,
        )
