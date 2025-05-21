from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Cuboid:

    def __init__(
        self, left: int, top: int, front: int, width: int, height: int, depth: int
    ) -> None:
        self.left = left
        self.top = top
        self.front = front
        self.width = width
        self.height = height
        self.depth = depth
