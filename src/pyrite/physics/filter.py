from __future__ import annotations

from typing import TYPE_CHECKING

from pymunk import ShapeFilter

if TYPE_CHECKING:
    from pyrite.types.aliases import CollisionGroup, ObjectCategory, CategoryMask


class Filter:
    """
    An object for determining and comparing collision between ColliderComponents.
    Objects with a shared group will not collide, nor will objects without matching
    masks.
    """

    def __init__(
        self, group: CollisionGroup, category: ObjectCategory, mask: CategoryMask
    ) -> None:
        self.group = group
        self.category = category
        self.mask = mask
        self._filter = ShapeFilter(group, category, mask)

    def rejects_collision(self, other: Filter) -> bool:
        """
        Determines if the filter refuse to collide with another filter.
        This will happen if they have the same non-zero group or if the masks don't
        align.

        :param other: Another filter object to be compared against.
        :return: True if the filters are incompatible, else False.
        """
        return (
            (self.group != 0 and self.group == other.group)
            or (self.category & other.mask) == 0
            or (self.mask & other.category) == 0
        )
