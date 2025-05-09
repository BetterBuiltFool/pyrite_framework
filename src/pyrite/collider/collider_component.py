from __future__ import annotations

from collections.abc import Sequence
from typing import Any, TYPE_CHECKING
from weakref import WeakKeyDictionary, WeakSet

from ..transform import Transform
from ..types import Component
from ..events import OnSeparate, OnTouch, WhileTouching

if TYPE_CHECKING:
    from ..types.shape import Shape


class ColliderComponent(Component):
    all_categories: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()
    collision_masks: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()
    colliders: WeakKeyDictionary[ColliderComponent, list[Shape]] = WeakKeyDictionary()
    transforms: WeakKeyDictionary[ColliderComponent, list[Transform]] = (
        WeakKeyDictionary()
    )

    def __init__(
        self,
        owner: Any,
        collider: Shape | Sequence[Shape],
        transform: Transform | Sequence[Transform] = None,
        layers: int = 1,
        collision_mask: int = 1,
    ) -> None:
        super().__init__(owner)

        if transform is None:
            # Make it a default transform
            transform = Transform()

        if not isinstance(collider, Sequence):
            collider = [collider]
        if not isinstance(transform, Sequence):
            # Use the same transform for all colliders if only one is provided.
            transform = [transform for _ in collider]

        self.colliders.setdefault(self, collider)
        self.transforms.setdefault(self, transform)

        self.categories.update({self: layers})
        self.collision_masks.update({self: collision_mask})

        self.is_touching: WeakSet[ColliderComponent] = WeakSet()
        self.was_touching: WeakSet[ColliderComponent] = WeakSet()

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
    def categories(self) -> int:
        return self.all_categories[self]

    def add_categories_layer(self, layer: int):
        self.categories[self] |= layer

    def remove_categories_layer(self, layer: int):
        self.categories[self] &= ~layer

    @property
    def collision_mask(self) -> int:
        return self.collision_masks[self]

    def add_collision_mask_layer(self, layer: int):
        self.collision_masks[self] |= layer

    def remove_collision_mask_layer(self, layer: int):
        self.collision_masks[self] &= ~layer

    def get_colliders(self) -> list[Shape]:
        return self.colliders[self]

    def get_transforms(self) -> list[Transform]:
        return self.transforms[self]

    def compare_mask(self, other: ColliderComponent) -> bool:
        return self.collision_mask & other.categories

    def collides_with(self, other: ColliderComponent) -> bool:
        """
        Determines if the two components share any overlap.

        :param other: Another ColliderComponent
        :return: True if the two components are overlapping and have compatible masks,
            otherwise False.
        """
        return other in self.is_touching

    def _flush_buffer(self):
        """
        Clears the last-frame collision buffer, and pushes the current frame buffer
        into it.
        """
        self.was_touching = self.is_touching.copy()
        self.is_touching = WeakSet()

    def add_collision(self, other_collider: ColliderComponent) -> bool:
        """
        Adds the other collider to the internal set of collisions this frame.

        :param other_collider: Another collider component determined to have collided
            with this one.
        :return: True if _other_collider_ is a new collision for this frame, otherwise
            False.
        """
        self.is_touching.add(other_collider)
        return other_collider not in self.was_touching
