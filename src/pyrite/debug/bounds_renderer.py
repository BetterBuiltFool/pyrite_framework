from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Color

from ..types.debug_renderer import DebugRenderer
from ..enum import RenderLayers
from ..rendering.camera_renderer import CameraRenderer
from ..rendering.viewport import Viewport

if TYPE_CHECKING:
    from pygame.typing import ColorLike
    from ..core.render_system import RenderQueue
    from ..camera import Camera


class BoundsRenderer(DebugRenderer):

    def __init__(self, draw_color: ColorLike) -> None:
        self.color = Color(draw_color)

    def draw_to_screen(self, cameras: Camera, render_queue: RenderQueue):
        for layer in RenderLayers._layers:
            layer_dict = render_queue.get(layer, {})
            for renderables in layer_dict.values():
                for renderable in renderables:
                    for camera in cameras:
                        bounds = renderable.get_bounds()
                        CameraRenderer.draw_rect(
                            camera,
                            Viewport.DEFAULT,
                            self.color,
                            bounds.get_rect(),
                            width=1,
                        )
