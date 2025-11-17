from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Rect

if TYPE_CHECKING:
    from pygame.typing import RectLike, Point
    from pyrite.types import CubeLike

    RectPoint = tuple[RectLike, Point]
    RectBased = tuple[RectLike, float, float]

    CuboidTuple = tuple[float, float, float, float, float, float]


class Cuboid:
    """
    Simple 3D shape for axis-aligned volumes
    """

    __slots__ = ("left", "top", "front", "width", "height", "depth")

    # TODO Add methods, properties as needed. This will suffice for now.

    def __init__(
        self,
        left: float | CubeLike,
        top: float = 0,
        front: float = 0,
        width: float = 0,
        height: float = 0,
        depth: float = 0,
    ) -> None:
        if isinstance(left, Cuboid):
            left, top, front, width, height, depth = self._deconstruct_cuboid(left)
        if isinstance(left, tuple):
            left, top, front, width, height, depth = self._deconstruct_tuple(left)

        self.left: float = left
        self.top = top
        self.front = front
        self.width = width
        self.height = height
        self.depth = depth

    @staticmethod
    def _deconstruct_cuboid(
        cuboid: Cuboid,
    ) -> CuboidTuple:
        return (
            cuboid.left,
            cuboid.top,
            cuboid.front,
            cuboid.width,
            cuboid.height,
            cuboid.depth,
        )

    @staticmethod
    def _deconstruct_tuple(cuboid: RectPoint | RectBased) -> CuboidTuple:
        if len(cuboid) == 2:
            front, depth = cuboid[1]
        elif len(cuboid) == 3:
            front, depth = cuboid[1], cuboid[2]
        elif len(cuboid) < 2:
            raise TypeError(
                f"Insufficient arguments, expected 2 or 3, got {len(cuboid)}"
            )
        else:
            raise TypeError(f"Too many arguments, expected 2 or 3, got {len(cuboid)}")
        try:
            rect = Rect(cuboid[0])
        except TypeError:
            raise TypeError(f"Expected RectLike value, received {cuboid[0]}")

        top, left = rect.topleft
        width, height = rect.size
        return left, top, front, width, height, depth

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Cuboid):
            return False
        return (
            value.top == self.top
            and value.left == self.left
            and value.front == self.front
            and value.width == self.width
            and value.height == self.height
            and value.depth == self.depth
        )
