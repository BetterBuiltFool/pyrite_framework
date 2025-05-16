from __future__ import annotations

from collections.abc import Sequence
from typing import Any, TYPE_CHECKING
from weakref import WeakKeyDictionary

from pymunk import ShapeFilter

from ..events import OnSeparate, OnTouch, WhileTouching
from .physics_service import PhysicsService, COMPONENT_TYPE
from .rigidbody_component import RigidbodyComponent
from ..types import Component

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

        self.OnTouch = OnTouch(self)
        """
        Called whenever a collider begins contact with another.

        :Signature:
        on_touch(this_collider: ColliderComponent, touching: ColliderComponent) -> None


        this_collider: The collider component belonging to the owner of the
            instance event.
        touching: The collider component in contact with _this_collider_
        """

        self.WhileTouching = WhileTouching(self)
        """
        Called every frame that two collider components overlap.

        :Signature:
        on_touch(this_collider: ColliderComponent, touching: ColliderComponent) -> None


        this_collider: The collider component belonging to the owner of the
            instance event.
        touching: The collider component in contact with _this_collider_
        """

        self.OnSeparate = OnSeparate(self)
        """
        Called whenever a previously touching collider stops touching.

        :Signature:
        on_separate(
            this_collider: ColliderComponent,
            touching: ColliderComponent
        ) -> None


        this_collider: The collider component belonging to the owner of the
            instance event.
        touching: The collider component formerly in contact with _this_collider_
        """

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
