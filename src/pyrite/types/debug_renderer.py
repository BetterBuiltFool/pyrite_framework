from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Surface
    from ..core.render_system import RenderQueue


class DebugRenderer(ABC):

    def draw_to_screen(self, window: Surface, render_queue: RenderQueue):
        """
        Gives the option to draw directly to the screen.

        :param window: _description_
        :param render_queue: _description_
        """
