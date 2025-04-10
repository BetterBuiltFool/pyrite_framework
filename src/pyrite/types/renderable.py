from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

from ._base_type import _BaseType

import pygame

if TYPE_CHECKING:
    from . import Container
    from .enums import Layer


class Renderable(_BaseType, ABC):
    """
    Base class for any renderable object in pyrite.
    """

    def __init__(
        self,
        container: Container = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
    ) -> None:
        self._layer: Layer = layer
        self.draw_index = draw_index
        """
        (The following is only true for default renderer; Others may vary)

        Indexer for draw order within a layer.
        Negative indexes are relative to the end.
        Renderables in the same layer with the same index may be drawn in any order.
        """
        _BaseType.__init__(self, container, enabled)

    @property
    def layer(self) -> Layer:
        return self._layer

    @layer.setter
    def layer(self, new_layer: Layer):
        if self._layer is not new_layer:
            enabled = self.enabled
            # This allows us to update within the renderer without firing
            # on enable/disable events.
            self.container.disable(self)
            self._layer = new_layer
            if enabled:
                self.container.enable(self)

    @abstractmethod
    def render(self, delta_time: float) -> pygame.Surface:
        """
        Supplies a surface ready to be blitted to another surface.

        :param delta_time: Time passed since last frame. Can be ignored by the concrete
        method but must be accepted.
        :return: A tuple containing a ready-to-draw surface and a rect with the
        position and size of the drawn area
        """
        pass

    @abstractmethod
    def get_rect(self) -> pygame.Rect:
        """
        Return a rectangle representing the area the rendered surface is expected to
        take up.

        :return: _description_
        """
        pass
