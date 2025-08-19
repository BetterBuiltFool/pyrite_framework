from __future__ import annotations

from collections.abc import Sequence
from typing import Any, TYPE_CHECKING
from weakref import WeakKeyDictionary

import pymunk
from pymunk import ShapeFilter

from ..events import OnSeparate, OnTouch, WhileTouching
from .rigidbody_component import RigidbodyComponent
from ..services import PhysicsService
from ..component import Component

if TYPE_CHECKING:
    from ..types.shape import Shape


class ColliderComponent(Component):
    """
    Component that manages collision shapes for a RigidbodyComponent.

    Has cooresponding events for collisions with other ColliderComponents.

    Uses bitmasks for controlling collisions.

    Requires RigidbodyComponent.

    ### Events:
    - OnTouch: Called on first contact with another ColliderComponent.
    - OnSeparate: Called when the ColliderComponent breaks contact with another.
    - WhileTouching: Called _every_ physics tick while contacting another
        ColliderComponent.
    """

    _categories: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()
    _collision_masks: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()

    def __init__(
        self,
        owner: Any,
        shape: Shape[pymunk.Shape] | Sequence[Shape[pymunk.Shape]],
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

        self.shapes: WeakKeyDictionary[Shape[pymunk.Shape], None] = WeakKeyDictionary()

        self.filter = ShapeFilter(categories=category, mask=mask)

        self.body = rigidbody.body

        PhysicsService.add_collider_shapes(self, shape)

        PhysicsService.add_collider(self)

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

    def _force_update_filter(self):
        self.filter = ShapeFilter(
            categories=self._categories[self], mask=self._collision_masks[self]
        )

    @property
    def category(self) -> int:
        """
        A bitmask showing the collision categories to which this collider belongs.
        Other colliders with any overlap in their collision mask will generate
        collision events.
        """
        return self._categories[self]

    def add_categories_layer(self, layer: int):
        """
        Takes a bitmask value and ensure that the Collider's category includes it.
        """
        self._categories[self] |= layer
        self._force_update_filter()

    def remove_categories_layer(self, layer: int):
        """
        Takes a bitmask value and ensures that the Collider's category excludes it.
        """
        self._categories[self] &= ~layer
        self._force_update_filter()

    @property
    def collision_mask(self) -> int:
        """
        A bitmask showing the collision layers with which this collider will generate
        events.
        """
        return self._collision_masks[self]

    def add_collision_mask_layer(self, layer: int):
        """
        Takes a bitmask value and ensure that the Collider's collision mask includes it.
        """
        self._collision_masks[self] |= layer
        self._force_update_filter()

    def remove_collision_mask_layer(self, layer: int):
        """
        Takes a bitmask value and ensures that the Collider's collision mask excludes
        it.
        """
        self._collision_masks[self] &= ~layer
        self._force_update_filter()

    def compare_mask(self, other: ColliderComponent) -> bool:
        """
        Compares the collision mask with the category of the other component to
        determine if they overlap.

        :param other: Another ColliderComponent.
        :return: True if the masks are overlapping, otherwise False.
        """
        return bool(self.collision_mask & other.category)
