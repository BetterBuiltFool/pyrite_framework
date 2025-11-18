from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from pygame import Rect

if TYPE_CHECKING:
    from pygame.typing import RectLike, Point
    from pyrite.types import CubeLike, _HasCuboidAttribute

    RectPoint = tuple[RectLike, Point]
    RectBased = tuple[RectLike, float, float]

    CuboidTuple = tuple[float, float, float, float, float, float]

    type _CubeLikeNoAttribute = (
        Cuboid
        # | SequenceLike[float]
        # | SequenceLike[Point3D]
        | tuple[RectLike, Point]
        | tuple[RectLike, float, float]
    )


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
        if hasattr(left, "cuboid"):
            # type:ignore being used here since the type checker doesn't notice that
            # _HasCuboidAttribute is the only valid match after this check.
            left = self._extract_cubelike_from_attribute(left)  # type:ignore
        if isinstance(left, Cuboid):
            left, top, front, width, height, depth = self._deconstruct_cuboid(left)
        elif isinstance(left, tuple):
            left, top, front, width, height, depth = self._deconstruct_tuple(left)
        else:  # temp for type control
            assert isinstance(left, (int, float))

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

    @staticmethod
    def _extract_cubelike_from_attribute(
        has_cuboid_attribute: _HasCuboidAttribute,
    ) -> _CubeLikeNoAttribute:
        """
        Takes an object with a `cuboid` attribute and extracts the cubelike value from
        it. Calls recursively if needed.

        :param has_cuboid_attribute: An object with a cuboid attribute, as defined by
            the _HasCuboidAttribute protocol.
        :return: A CubeLike object that isn't _HasCuboidAttribute.
        """
        cube_like = has_cuboid_attribute.cuboid
        if isinstance(cube_like, Callable):
            # _HasCuboidAttribute
            cube_like = cube_like()
        if hasattr(cube_like, "cuboid"):
            # Recursive check, incase somehow we end up with a multi-layer-deep
            # nest of _HasCuboidAttributes.
            # Worth note that this will be a problem if the nesting is infinite,
            # of course.

            # Using type ignore only because the type checker doesn't recognize that
            # hasattr already filtered out the cases without the attribute.
            cube_like = Cuboid._extract_cubelike_from_attribute(
                cube_like  # type:ignore
            )

        # Again, tpye:ignore because we've established that there is no
        # _HasCuboidAttribute remaining.
        return cube_like  # type:ignore

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


if TYPE_CHECKING:
    del _CubeLikeNoAttribute
