from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any
from weakref import WeakKeyDictionary

from ..types import Component

if TYPE_CHECKING:
    from ..types.collider import Collider
    from ..transform import Transform


class ColliderComponent(Component):
    layers: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()
    collision_masks: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()
    colliders: WeakKeyDictionary[ColliderComponent, list[Collider]] = (
        WeakKeyDictionary()
    )
    transforms: WeakKeyDictionary[ColliderComponent, list[Transform]] = (
        WeakKeyDictionary()
    )

    def __init__(
        self,
        owner: Any,
        colliders: Collider | Sequence[Collider],
        transforms: Transform | Sequence[Transform],
        layers: int,
        collision_mask: int,
    ) -> None:
        super().__init__(owner)

        if not isinstance(colliders, Sequence):
            colliders = list(colliders)
        if not isinstance(transforms, Sequence):
            # Use the same transform for all colliders if only one is provided.
            transforms = [transforms for _ in colliders]

        self.colliders.setdefault(self, colliders)
        self.transforms.setdefault(self, transforms)

        self.layers.update({self: layers})
        self.collision_masks.update({self: collision_mask})

    def get_colliders(self) -> list[Collider]:
        return self.colliders[self]
