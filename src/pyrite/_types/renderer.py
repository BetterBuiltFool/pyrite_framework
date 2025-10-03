from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Renderer[RenderableTypeT, RenderTargetT](ABC):

    @abstractmethod
    def render(self, renderable: RenderableTypeT, target: RenderTargetT):
        """
        Draws the renderable to the screen.

        :param renderable: The renderable item, of the type handled by the renderer.
        :param target: An object to render to.
        """
        pass


class RendererProvider[ProvidedRendererT: Renderer](ABC):
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
