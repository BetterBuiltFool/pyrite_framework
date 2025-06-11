from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
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
        self.font = pygame.font.Font()

    def draw_to_screen(self, cameras: Camera, render_queue: RenderQueue):
        for layer in RenderLayers._layers:
            layer_dict = render_queue.get(layer, {})
            for renderables in layer_dict.values():
                for renderable in renderables:
                    bounds = renderable.get_bounds()
                    bounds_rect = bounds.get_rect()
                    for camera in cameras:
                        center = CameraRenderer._world_to_screen(
                            bounds_rect.center, camera, Viewport.DEFAULT
                        )
                        rendered_text = self.font.render(
                            f"World: {bounds_rect.center}\nScreen: {center}",
                            False,
                            Color("gray"),
                        )
                        display = Viewport.DEFAULT.get_target_surface()
                        pygame.draw.circle(
                            display,
                            Color("white"),
                            center,
                            1,
                        )
                        pygame.draw.line(
                            display,
                            Color("darkgray"),
                            center,
                            display.get_rect().center,
                        )
                        display.blit(rendered_text, center)
                        # CameraRenderer.draw_rect(
                        #     camera,
                        #     Viewport.DEFAULT,
                        #     self.color,
                        #     bounds_rect,
                        #     width=1,
                        # )
