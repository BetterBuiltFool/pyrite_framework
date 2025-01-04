from abc import abstractmethod, ABC

from ._base_type import _BaseType
from src.pyrite.types.enums import Layer

import pygame


class Renderable(_BaseType, ABC):
    """
    Base class for any renderable object in pyrite.
    """

    def __init__(
        self, game_instance=None, enabled=True, layer: Layer = None, draw_index=-1
    ) -> None:
        self.layer: Layer = layer
        self.draw_index = draw_index
        super().__init__(game_instance, enabled)

    @abstractmethod
    def render(
        self, delta_time: float
    ) -> tuple[pygame.Surface, pygame.typing.Point | pygame.Rect]:
        """
        Supplies a surface ready to be blitted to another surface.

        :param delta_time: Time passed since last frame. Can be ignored by the concrete
        method but must be accepted.
        :return: A tuple containing a ready-to-draw surface and a point with relative
        location
        """
        pass


class UIElement(_BaseType, ABC):

    @abstractmethod
    def render_ui(
        self, delta_time: float
    ) -> tuple[pygame.Surface, pygame.typing.Point | pygame.Rect]:
        """
        Supplies a surface ready to be blitted to another surface. Drawn late during
        the render_ui phase, so it will always be drawn over any other renderings.

        :param delta_time: Time passed since last frame. Can be ignored by the concrete
        method but must be accepted.
        :return: A tuple containing a ready-to-draw surface and a point with relative
        location
        """
        pass
