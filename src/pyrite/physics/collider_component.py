from __future__ import annotations

from collections.abc import Sequence
from typing import Any, TYPE_CHECKING
from weakref import WeakKeyDictionary

from ..types import Component
from .rigidbody import RigidbodyComponent
from .physics_service import PhysicsService

if TYPE_CHECKING:
    from pymunk import Shape


class ColliderComponent(Component):
    _categories: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()
    _collision_masks: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()

    def __init__(
        self,
        owner: Any,
        shape: Shape | Sequence[Shape],
        category: int = 1,
        mask: int = None,
    ) -> None:
        super().__init__(owner)
        if not (rigidbody := RigidbodyComponent.get(owner)):
            raise RuntimeError(
                f"ColliderComponent requires that {owner} has a RigidbodyComponent"
            )
        if not isinstance(shape, Sequence):
            shape = [shape]

        self._categories.update({self: category})
        self._collision_masks.update({self: mask})

        self.shapes = shape

        body = rigidbody.body
        for collision_shape in shape:
            collision_shape.body = body
            PhysicsService.space.add(collision_shape)

    @property
    def category(self) -> int:
        return self._categories[self]

    def add_categories_layer(self, layer: int):
        self._categories[self] |= layer

    def remove_categories_layer(self, layer: int):
        self._categories[self] &= ~layer

    @property
    def collision_mask(self) -> int:
        return self._collision_masks[self]

    def add_collision_mask_layer(self, layer: int):
        self._collision_masks[self] |= layer

    def remove_collision_mask_layer(self, layer: int):
        self._collision_masks[self] &= ~layer

    def compare_mask(self, other: ColliderComponent) -> bool:
        return self.collision_mask & other.category
