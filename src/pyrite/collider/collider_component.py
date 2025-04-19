from __future__ import annotations

from typing import TYPE_CHECKING, Any
from weakref import WeakKeyDictionary

from ..types import Component

if TYPE_CHECKING:
    from ..types.collider import Collider


class ColliderComponent(Component):
    layers: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()
    collision_masks: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()
    colliders: WeakKeyDictionary[ColliderComponent, Collider] = WeakKeyDictionary()

    def __init__(
        self, owner: Any, collider: Collider, layers: int, collision_mask: int
    ) -> None:
        super().__init__(owner)
        self.colliders.update({self: collider})
        self.layers.update({self: layers})
        self.collision_masks.update({self: collision_mask})

    @property
    def collider(self) -> Collider:
        return self.colliders[self]
