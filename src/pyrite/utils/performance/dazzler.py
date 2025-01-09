from __future__ import annotations

import random
from typing import TYPE_CHECKING

from src.pyrite.types.entity import Entity
from src.pyrite.types.renderable import Renderable

from src.pyrite.types.enums import RenderLayers

import pygame
from pygame import Surface, Rect

if TYPE_CHECKING:
    from src.pyrite.types import Container
    from pygame.typing import Point


class Dazzler(Entity, Renderable):
    """
    A simple renderable entity with a semi-complex render step to to stress-test the
    framework.
    """

    def __init__(
        self,
        position: Point = (0, 0),
        container: Container = None,
        enabled=True,
        draw_index=0,
    ) -> None:
        super().__init__(container, enabled, RenderLayers.BACKGROUND, draw_index)
        self.counter = 0
        self.surface = Surface((32, 32))
        self.surface.fill(pygame.Color("white"))
        self.subsurface = Surface((8, 8))
        self.position = pygame.Vector2(position)

    def const_update(self, timestep: float) -> None:
        if self.counter > 5:
            return
        self.counter += 1

    def get_rect(self) -> Rect:
        return self.surface.get_rect(center=self.position)

    def render(self, delta_time: float) -> tuple[Surface, Rect]:
        if self.counter > 5:
            self.counter = 0
            self.surface.fill(pygame.Color("white"))
            for _ in range(3):
                x = random.randrange(0, 24, 8)
                y = random.randrange(0, 24, 8)
                # Random bright color
                color = pygame.Color(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )
                self.subsurface.fill(color)
                self.surface.blit(self.subsurface, (x, y))
        return (self.surface, self.get_rect())

    @staticmethod
    def multispawn(number_spawns, area: pygame.typing.RectLike) -> set[Dazzler]:
        """
        Creates a number of Dazzlers randomly distributed within a rectangular area.

        :param number_spawns: Number of Dazzlers to be spawned
        :param area: Rectangular area to spawn the Dazzlers in
        :return: A set containing the spawned Dazzlers.
        """
        area = Rect(area)
        min_x, min_y = area.topleft
        size_x, size_y = area.size
        max_x = min_x + size_x
        max_y = min_y + size_y
        return {
            Dazzler(
                position=(
                    random.randrange(min_x, max_x, 32),
                    random.randrange(min_y, max_y, 32),
                )
            )
            for _ in range(number_spawns)
        }
