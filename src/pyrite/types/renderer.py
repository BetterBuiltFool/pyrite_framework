from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, TYPE_CHECKING
from weakref import WeakSet

from src.pyrite.types.renderable import Renderable
from src.pyrite.types.enums import Layer, RenderLayers

if TYPE_CHECKING:
    from src.pyrite.types._base_type import _BaseType

import pygame


class Renderer(ABC):

    @abstractmethod
    def generate_render_queue(self) -> dict[Any, Sequence[Renderable]]:
        """
        Generates a dict of renderables, in draw order.

        The keys are metadata used by the renderer to determine factors like layer
        culling and, partially, draw order. They can be of any type, but must be a type
        the render method knows how to handle.
        """
        pass

    @abstractmethod
    def render(
        self, surface: pygame.Surface, renderables: dict[Any, Sequence[Renderable]]
    ):
        """
        Draws the items from the renderable dictionary onto the passed surface.

        :param surface: The surface receiving the final draws, typically the window
        :param renderables: A list of items that need to be rendered to the surface.
        """
        pass

    @abstractmethod
    def enable(self, item: _BaseType):
        """
        Adds a Renderable to the collection of renderables.

        Does nothing if the item is not a renderable.

        :param item: Object being enabled. Must be a renderable to properly register.
        """
        pass

    @abstractmethod
    def disable(self, item: _BaseType):
        """
        Removes the item from the collection of renderables.

        :param item: Renderable being removed.
        """
        pass


def get_draw_index(renderable: Renderable) -> int:
    return renderable.draw_index


class DefaultRenderer(Renderer):
    """
    TODO Add cameras. Give a special layer that's always last.
    In the render phase, extract any cameras, draw to them, and then draw them to the
    screen (That's why they're last.)

    :param Renderer: _description_
    """

    def __init__(self) -> None:
        self.renderables: dict[Layer, WeakSet[Renderable]] = {}

    def enable(self, item: _BaseType):
        if not isinstance(item, Renderable):
            return
        layer = item.layer
        if layer is None:
            # No layer set, force it to midground
            layer = RenderLayers.MIDGROUND
            item.layer = layer
        self.renderables.update({layer: item})

    def disable(self, item: _BaseType):
        if not isinstance(item, Renderable):
            return
        layer = item.layer
        self.renderables.get(layer, set()).discard(item)

    def generate_render_queue(self) -> dict[Layer, Sequence[Renderable]]:
        render_queue = {layer: [] for layer in RenderLayers._layers}
        for layer in RenderLayers._layers:
            render_queue.update(
                # This looks nasty, but comps are fast.
                # Basically, create a list from the set of renderables in a layer, and
                # then sorts it by draw_index
                {layer, list(self.renderables.get(layer, {})).sort(key=get_draw_index)}
            )
        return render_queue

    def render(
        self, surface: pygame.Surface, renderables: dict[Layer, Sequence[Renderable]]
    ):
        for layer in RenderLayers._layers:
            # _layers is sorted by desired draw order.
            layer_queue = renderables.get(layer, [])
            # TODO fix delta time issue here
            surface.blits([renderable.render() for renderable in layer_queue])
