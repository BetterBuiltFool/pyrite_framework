from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Camera

RenderableTypeT = TypeVar("RenderableTypeT")


class Renderer(ABC, Generic[RenderableTypeT]):

    @abstractmethod
    def render(self, delta_time: float, renderable: RenderableTypeT, camera: Camera):
        """
        Draws the renderable to the screen via the camera object.

        :param delta_time: Time passed since last frame
        :param renderable: The renderable item, of the type handled by the renderer.
        :param camera: A Camera object, used for determining screen space position.
        """
        pass


ProvidedRendererT = TypeVar("ProvidedRendererT", bound=Renderer)


class RendererProvider(ABC, Generic[ProvidedRendererT]):
    """
    Accessor class for a given renderer. Delegates methods to the renderer instance,
    providing an access point to the users of that renderer while allowing the instance
    to be swapped with variants at runtime.
    """

    _renderer: ProvidedRendererT

    @classmethod
    @abstractmethod
    def hotswap(cls, renderer: ProvidedRendererT):
        """
        Changes over the renderer instance, and transfers and required data that is
        shared between the two.

        :param renderer: The new renderer instance.
        """
        pass
