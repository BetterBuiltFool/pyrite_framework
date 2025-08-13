from __future__ import annotations

from typing import TYPE_CHECKING

import pymunk

from pygame import Rect, Vector2

# from ..utils import point_to_tuple

if TYPE_CHECKING:
    # from pygame.typing import Point

    from weakref import ref
    from ..physics import ColliderComponent, RigidbodyComponent


class Shape[ShapeT: pymunk.Shape]:

    def __init__(self) -> None:
        self._rigidbody: RigidbodyComponent | None
        self._collider: ref[ColliderComponent] | None
        self._shape: ShapeT

    @property
    def area(self) -> float:
        return self._shape.area

    @property
    def bounding_box(self) -> Rect:
        bb = self._shape.bb
        left, top, right, bottom = bb.left, bb.top, bb.right, bb.bottom
        width = right - left
        height = top - bottom
        return Rect(left, top, width, height)

    @property
    def collider(self) -> ColliderComponent | None:
        """
        The ColliderComponent the shape is attached to. If None, the shape is not
        attached to any rigidbody.

        :return: A ColliderComponent, or None if unattached.
        """
        if self._collider:
            return self._collider()
        return None

    @collider.setter
    def collider(self, collider: ColliderComponent | None) -> None:
        if self.collider is not None:
            # del self.collider.shapes[self]
            pass
        if collider is None:
            self._collider = None
            return
        self._collider = ref(collider)
        # collider.shapes[self] = None

    @property
    def center_of_gravity(self) -> Vector2:
        """
        Returns the calculated center of gravity for this shape.
        """
        return Vector2(self._shape.center_of_gravity)
