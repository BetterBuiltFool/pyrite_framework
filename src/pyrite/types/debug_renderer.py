from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ..camera import Camera
    from ..core.render_system import RenderQueue


class DebugRenderer(ABC):

    def draw_to_screen(self, cameras: Sequence[Camera], render_queue: RenderQueue):
        """
        Gives the option to draw directly to the screen.

        :param cameras: A sequence of cameras to be drawn to.
        :param render_queue: The queue of renderables on the screen when called.
        """
