from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from weakref import WeakSet

from src.pyrite.types.renderable import Renderable
from src.pyrite.types.enums import Layer, RenderLayers

if TYPE_CHECKING:
    from src.pyrite.types._base_type import _BaseType

import pygame


class Renderer(ABC):

    @abstractmethod
    def generate_render_queue(self):
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface):
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


class DefaultRenderer(Renderer):

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
