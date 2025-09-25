from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pyrite._types.camera import Camera
    from pyrite.core.render_system import RenderQueue


class DebugRenderer(ABC):
    """
    Abstract class for special renderers that draw after the cameras have rendered,
    useful for overlaying debug info on the screen.
    """

    def draw_to_screen(self, cameras: Iterable[Camera], render_queue: RenderQueue):
        """
        Gives the option to draw directly to the screen.

        :param cameras: The sequence of available cameras being rendered this frame.
            Will always contain at least one camera, the Default camera if no others
            are active.
        :param render_queue: The queue of renderables on the screen when called.
        """
