from __future__ import annotations

from pygame.typing import Point
from pygame import Vector2


class Transform:

    def __init__(self, position: Point) -> None:
        self.position = Vector2(position)
