from abc import abstractmethod, ABC

from ._base_type import _BaseType
from src.pyrite.types.enums import Layer

import pygame


class Renderable(_BaseType, ABC):
    """
    Base class for any renderable object in pyrite.
    """

    def __init__(
        self, game_instance=None, enabled=True, layer: Layer = None, draw_index=0
    ) -> None:
        self.layer: Layer = layer
        self.draw_index = draw_index
        """
        (The following is only true for default renderer; Others may vary)

        Indexer for draw order within a layer.
        Negative indexes are relative to the end.
        Renderables in the same layer with the same index may be drawn in any order.
        """
        super().__init__(game_instance, enabled)

    @abstractmethod
    def render(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]:
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
