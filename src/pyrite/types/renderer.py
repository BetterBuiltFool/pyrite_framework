from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Renderable, CameraBase


class Renderer(ABC):

    @abstractmethod
    def cull(self, renderable: Renderable, camera: CameraBase) -> bool:
        """
        Compares the renderable to the camera to determine if the renderable is visible
        and thus should be rendered.

        :param renderable: The renderable item, of the type handled by the renderer.
        :param camera: A CameraBase, to which the cull check is being performed.
        :return: True if the camera can see the renderable, otherwise False.
        """
        pass

    @abstractmethod
    def render(self, renderable: Renderable, camera: CameraBase):
        """
        Draws the renderable to the screen via the camera object.

        :param renderable: The renderable item, of the type handled by the renderer.
        :param camera: A CameraBase, used for determining screen space position.
        """
        pass
