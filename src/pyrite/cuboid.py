from __future__ import annotations

from typing import overload, TYPE_CHECKING

from pygame import Rect

from pyrite.types import (
    has_cubelike_attribute,
    has_rect_like,
    is_sequence_based,
    is_number_sequence,
    is_3d_points,
)

if TYPE_CHECKING:
    from pyrite.types import (
        CubeLike,
        _HasCuboidAttribute,
        CuboidTuple,
        _SequenceBased,
        _CubeLikeNoAttribute,
    )

BAD_CUBELIKE_EXCEPTION = TypeError("Expected Cuboid-style object")


class Cuboid:
    """
    Simple 3D shape for axis-aligned volumes
    """

    __slots__ = ("left", "top", "front", "width", "height", "depth")

    # TODO Add methods, properties as needed. This will suffice for now.

    @overload
    def __init__(
        self,
        left: float = 0,
        top: float = 0,
        front: float = 0,
        width: float = 0,
        height: float = 0,
        depth: float = 0,
    ) -> None: ...

    @overload
    def __init__(self, cubelike: CubeLike) -> None: ...

    def __init__(  # type:ignore
        self,
        left: float | CubeLike = 0,
        top: float = 0,
        front: float = 0,
        width: float = 0,
        height: float = 0,
        depth: float = 0,
        cubelike: CubeLike | None = None,  # To handle keyword passing
    ) -> None:
        if cubelike is not None:
            left = cubelike
        if has_cubelike_attribute(left):
            left = self._extract_cubelike_from_attribute(left)
        if isinstance(left, Cuboid):
            left, top, front, width, height, depth = self._deconstruct_cuboid(left)
        elif is_sequence_based(left):
            left, top, front, width, height, depth = self._deconstruct_sequence(left)
        elif not isinstance(left, (int, float)):
            raise BAD_CUBELIKE_EXCEPTION

        self.left = left
        self.top = top
        self.front = front
        self.width = width
        self.height = height
        self.depth = depth

    @property
    def right(self) -> float:
        """
        X coordinate of the right-most side of the cuboid.
        """
        return self.left + self.width

    @right.setter
    def right(self, right: float) -> None:
        self.left = right - self.width

    @property
    def bottom(self) -> float:
        """
        Y Coordinate of the bottom-most side of the cuboid.
        """
        return self.top + self.height

    @bottom.setter
    def bottom(self, bottom: float) -> None:
        self.top = bottom - self.height

    @property
    def back(self) -> float:
        """
        Z Coordinate of the back-most side of the cuboid.
        """
        return self.front + self.depth

    @back.setter
    def back(self, back: float) -> None:
        self.front = back - self.depth

    @property
    def face_xy(self) -> Rect:
        """
        Represents the face of the cuboid in like with the xy plane.

        :return: A Rect that matches the cuboid's left, top, width, and height
        """
        return Rect(self.left, self.top, self.width, self.height)

    @property
    def face_xz(self) -> Rect:
        """
        Represents the face of the cuboid in like with the xz plane.

        :return: A Rect that matches the cuboid's left, front, width, and depth
        """
        return Rect(self.left, self.front, self.width, self.depth)

    @property
    def face_yz(self) -> Rect:
        """
        Represents the face of the cuboid in like with the yz plane.

        :return: A Rect that matches the cuboid's top, front, height, and depth
        """
        return Rect(self.top, self.front, self.height, self.depth)

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
    def _deconstruct_sequence(cuboid: _SequenceBased) -> CuboidTuple:
        if is_number_sequence(cuboid):
            left, top, front, width, height, depth = cuboid
        elif is_3d_points(cuboid):
            left, top, front = cuboid[0]
            width, height, depth = cuboid[1]
        elif has_rect_like(cuboid):
            if len(cuboid) == 2:
                front, depth = cuboid[1]
            elif len(cuboid) == 3:
                front, depth = cuboid[1], cuboid[2]
            else:
                raise BAD_CUBELIKE_EXCEPTION
            try:
                rect = Rect(cuboid[0])
            except TypeError:
                raise BAD_CUBELIKE_EXCEPTION

            left, top = rect.topleft
            width, height = rect.size
        else:
            raise BAD_CUBELIKE_EXCEPTION

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
        if callable(cube_like):
            cube_like = cube_like()
        if has_cubelike_attribute(cube_like):
            # Recursive check, incase somehow we end up with a multi-layer-deep
            # nest of _HasCuboidAttributes.
            # Worth note that this will be a problem if the nesting is infinite,
            # of course.
            cube_like = Cuboid._extract_cubelike_from_attribute(cube_like)

        # Currently in python 3.12, so TypeIs is not available, and TypeGuard isn't
        # smart enough to determine that there can no longer be a _HasCuboidAttribute.
        # Need to use type:ignore to get around this.
        # TODO: Update python and switch to TypeIs
        return cube_like  # type:ignore

    def __getitem__(self, index: int) -> float:
        value_dict: dict[int, float] = {
            0: self.left,
            1: self.top,
            3: self.front,
            4: self.width,
            5: self.height,
            6: self.depth,
        }
        return value_dict[index]

    def __len__(self) -> int:
        return 6

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
