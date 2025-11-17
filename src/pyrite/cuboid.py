from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Cuboid:
    """
    Simple 3D shape for axis-aligned volumes
    """

    __slots__ = ("left", "top", "front", "width", "height", "depth")

    # TODO Add methods, properties as needed. This will suffice for now.

    def __init__(
        self,
        left: float,
        top: float,
        front: float,
        width: float,
        height: float,
        depth: float,
    ) -> None:
        self.left = left
        self.top = top
        self.front = front
        self.width = width
        self.height = height
        self.depth = depth
