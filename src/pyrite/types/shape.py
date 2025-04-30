from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pygame import Rect, Vector2
from ..transform import Transform

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.typing import ColorLike

DIRECTIONS: list[Vector2] = [
    Vector2(0, -1),  # Up, 0
    Vector2(1, 0),  # Right, 1
    Vector2(0, 1),  # Down, 2
    Vector2(-1, 0),  # Left, 3
]


class Shape(ABC):

    def get_aabb(self, transform: Transform = None) -> Rect:
        """
        Returns an axis-aligned bounding box for the collider.

        :transform: A Transform object representing the center of the collider in world
            space. If None, will use a default transform.
        """
        if transform is None:
            transform = Transform()
        extents = self._get_extents(transform)
        top = extents[0].y
        left = extents[3].x
        height = extents[2].y - top
        width = extents[1].x - left
        return Rect(left, top, width, height)

    @abstractmethod
    def get_furthest_vertex(self, vector: Vector2, transform: Transform) -> Vector2:
        """
        Gets the furthest point of the shape in the direction provided by the vector

        :param vector: A normalized vector indicating a direction
        :param transform: A transform indicating the world-space center of the collider.
        :return: A position, in world space, representing the furthest point in that
            direction.
        """
        pass

    @abstractmethod
    def get_vertices(self) -> tuple[Vector2]:
        """
        Returns a list of vertices (for polygons) or critical points (for shapes with
        curves), relative to the shape's center.
        """
        pass

    @abstractmethod
    def draw(
        self,
        edge_width: int = 1,
        edge_color: ColorLike = None,
        fill_color: ColorLike = None,
    ) -> Surface:
        pass

    def _get_extents(self, transform: Transform) -> list[Vector2]:
        extents: list[Vector2] = []
        for direction in DIRECTIONS:
            extents.append(self.get_furthest_vertex(direction, transform))
        return extents

    def _prescale_vector(self, vector: Vector2, transform: Transform) -> Vector2:
        """
        Performs a standard translation of a vector into local space of the transform.

        :param vector: A direction vector
        :param transform: A transform representing localization data for the vector
        :return: The corrected vector, normalized
        """
        vector = vector.elementwise() / transform.scale
        vector = vector.rotate(-transform.rotation)
        return vector.normalize()
