from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from . import CameraBase

RenderableType = TypeVar("RenderableType")


class Renderer(ABC, Generic[RenderableType]):

    @classmethod
    @abstractmethod
    def render(self, delta_time: float, renderable: RenderableType, camera: CameraBase):
        """
        Draws the renderable to the screen via the camera object.

        :param delta_time: Time passed since last frame
        :param renderable: The renderable item, of the type handled by the renderer.
        :param camera: A CameraBase, used for determining screen space position.
        """
        pass
