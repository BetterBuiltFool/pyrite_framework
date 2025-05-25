from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Color

from ..types.debug_renderer import DebugRenderer

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.typing import ColorLike
    from ..core.render_system import LayerDict, RenderQueue


class BoundsRenderer(DebugRenderer):

    def __init__(self, draw_color: ColorLike) -> None:
        self.color = Color(draw_color)

    def render(self, *args, **kwds):
        window: Surface = kwds["window"]
        render_queue: RenderQueue = kwds["render_queue"]
        if not window or not render_queue:
            return
        layer_dict: LayerDict
        for layer_dict in render_queue.values():
            for renderables in layer_dict.values():
                for renderable in renderables:
                    bounds = renderable.get_bounds()
                    pygame.draw.rect(window, self.color, bounds.get_rect(), width=1)
