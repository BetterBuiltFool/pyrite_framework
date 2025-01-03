from __future__ import annotations

from abc import ABC, abstractmethod
from weakref import WeakSet

from src.pyrite.types.renderable import Renderable

import pygame


class Renderer(ABC):

    @abstractmethod
    def generate_render_queue(self):
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface):
        pass

    @abstractmethod
    def enable(self, item: Renderable):
        pass

    @abstractmethod
    def disable(self, item: Renderable):
        pass


class DefaultRenderer(Renderer):

    def __init__(self) -> None:
        self.renderables: dict[WeakSet[Renderable]] = {}
