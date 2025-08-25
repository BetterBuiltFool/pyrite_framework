from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrite.types.aliases import CollisionGroup, ObjectCategory, CategoryMask


class Filter:

    def __init__(
        self, group: CollisionGroup, category: ObjectCategory, mask: CategoryMask
    ) -> None:
        self.group = group
        self.category = category
        self.mask = mask

    def rejects_collision(self, other: Filter) -> bool:
        return (
            (self.group != 0 and self.group == other.group)
            or (self.category & other.mask) == 0
            or (self.mask & other.category) == 0
        )
