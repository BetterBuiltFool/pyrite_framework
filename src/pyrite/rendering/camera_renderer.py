from __future__ import annotations

from typing import TYPE_CHECKING

from ..types import Renderer

if TYPE_CHECKING:
    from ..types import CameraBase
    from ..camera import Camera


class CameraRenderer(Renderer):

    @classmethod
    def render(cls, camera: Camera, window_camera: CameraBase):
        for sector in camera.surface_sectors:
            render_rect = sector.get_rect(window_camera.surface)
            window_camera.draw_to_view(
                camera.scale_view(camera.surface, render_rect.size), render_rect.topleft
            )
