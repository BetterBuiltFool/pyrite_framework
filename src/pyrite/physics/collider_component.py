from __future__ import annotations

from collections.abc import Sequence
from typing import Any, TYPE_CHECKING
from weakref import WeakKeyDictionary

import cffi
from pymunk import ShapeFilter

from ..types import Component
from .rigidbody_component import RigidbodyComponent
from .physics_service import PhysicsService

if TYPE_CHECKING:
    from pymunk import Shape


# Calculating the system's max int value for setting the collision type of
# ColliderComponents
COMPONENT_TYPE: int = 2 ** (cffi.FFI().sizeof("int") * 8 - 1) - 1


class ColliderComponent(Component):
    _categories: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()
    _collision_masks: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()

    def __init__(
        self,
        owner: Any,
        shape: Shape | Sequence[Shape],
        category: int = 1,
        mask: int = 0xFFFFFFFF,  # Pymunk provided max value
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

        self.filter = ShapeFilter(categories=category, mask=mask)

        body = rigidbody.body
        for collision_shape in shape:
            collision_shape.collision_type = COMPONENT_TYPE
            collision_shape.body = body
            collision_shape.filter = self.filter
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

    def _set_shape_filter(self):
        self.filter = ShapeFilter(categories=self.category, mask=self.collision_mask)
        for shape in self.shapes:
            shape.filter = self.filter
