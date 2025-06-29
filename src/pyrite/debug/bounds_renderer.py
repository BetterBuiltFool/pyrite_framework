from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Color

from ..types.debug_renderer import DebugRenderer
from ..enum import RenderLayers
from .. import draw

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pygame.typing import ColorLike
    from ..core.render_system import RenderQueue
    from ..types import Camera


class BoundsRenderer(DebugRenderer):

    def __init__(self, draw_color: ColorLike) -> None:
        self.color = Color(draw_color)
        self.font = pygame.font.Font()

    def draw_to_screen(self, cameras: Iterable[Camera], render_queue: RenderQueue):
        for layer in RenderLayers._layers:
            layer_dict = render_queue.get(layer, {})
            for renderables in layer_dict.values():
                for renderable in renderables:
                    bounds = renderable.get_bounds()
                    bounds_rect = bounds.get_rect()
                    for camera in cameras:
                        for viewport in camera.get_viewports():
                            draw.rect(
                                camera,
                                viewport,
                                self.color,
                                bounds_rect,
                                width=1,
                            )
