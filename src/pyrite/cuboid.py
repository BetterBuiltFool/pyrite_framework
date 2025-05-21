from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Cuboid:
    """
    Simple 3D shape for axis-aligned volumes
    """

    # TODO Add methods, properties as needed. This will suffice for now.

    def __init__(
        self, left: int, top: int, front: int, width: int, height: int, depth: int
    ) -> None:
        self.left = left
        self.top = top
        self.front = front
        self.width = width
        self.height = height
        self.depth = depth
