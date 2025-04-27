from __future__ import annotations

from collections.abc import Sequence
from typing import Any, TYPE_CHECKING
from weakref import WeakKeyDictionary, WeakSet

from ..types import Component
from ..events import OnTouch, WhileTouching
from ..transform.transform_component import TransformComponent
from .. import collider

if TYPE_CHECKING:
    from ..types.collider import Collider
    from ..transform import Transform


class ColliderComponent(Component):
    layer_masks: WeakKeyDictionary[ColliderComponent, int] = WeakKeyDictionary()
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
            colliders = [colliders]
        if not isinstance(transforms, Sequence):
            # Use the same transform for all colliders if only one is provided.
            transforms = [transforms for _ in colliders]

        self.colliders.setdefault(self, colliders)
        self.transforms.setdefault(self, transforms)

        self.layer_masks.update({self: layers})
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

    @property
    def layer_mask(self) -> int:
        return self.layer_masks[self]

    @property
    def collision_mask(self) -> int:
        return self.collision_masks[self]

    def get_colliders(self) -> list[Collider]:
        return self.colliders[self]

    def get_transforms(self) -> list[Transform]:
        return self.transforms[self]

    def compare_mask(self, other: ColliderComponent) -> bool:
        return self.collision_mask & other.layer_mask

    def _flush_buffer(self):
        """
        Clears the last-frame collision buffer, and pushes the current frame buffer
        into it.
        """
        self.was_touching = self.is_touching
        self.is_touching = WeakSet()

    def collides_with(self, other_component: ColliderComponent) -> bool:
        """
        Determines if there is overlap with _other_collider_

        :param other_component: Another collider component that is a potential overlap.
        :return: True if the components have any overlapping colliders.
        """
        this_transform = TransformComponent.get(self.owner)
        other_transform = TransformComponent.get(other_component.owner)
        return any(
            collider.collide(
                collider_a,
                collider_b,
                this_transform * transform_a,
                other_transform * transform_b,
            )
            for collider_b, transform_b in zip(
                other_component.get_colliders(), other_component.get_transforms()
            )
            for collider_a, transform_a in zip(
                self.get_colliders(), self.get_transforms()
            )
        )

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
