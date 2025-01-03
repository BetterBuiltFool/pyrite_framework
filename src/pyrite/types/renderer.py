from __future__ import annotations

from abc import ABC, abstractmethod


class Renderer(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def generate_render_queue(self):
        pass

    @abstractmethod
    def render(self, surface):
        pass
