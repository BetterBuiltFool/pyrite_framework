from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..types import System
from .collider_component import ColliderComponent
from ..transform import TransformComponent

if TYPE_CHECKING:
    from ..types.collider import Collider
    from ..transform import Transform


class ColliderSystem(System):

    def post_update(self, delta_time: float) -> None:
        colliding_objects = list(ColliderComponent.intersect(TransformComponent))

        colliders = {
            colliding_object: ColliderComponent.get(colliding_object).collider
            for colliding_object in colliding_objects
        }

        transforms = {
            colliding_object: TransformComponent.get(colliding_object).world()
            for colliding_object in colliding_objects
        }

        first_pass_candidates = self.get_first_pass_collisions(  # noqa:F841
            colliding_objects, colliders, transforms
        )

    def get_first_pass_collisions(
        self,
        colliding_objects: list[Any],
        colliders: dict[Any, Collider],
        transforms: dict[Any, Transform],
    ) -> dict[ColliderComponent, list[ColliderComponent]]:
        first_pass_candidates: dict[ColliderComponent, list[ColliderComponent]] = {}

        aabbs = {
            colliding_object: colliders[colliding_object].get_aabb(
                transforms[colliding_object]
            )
            for colliding_object in colliding_objects
        }

        length = len(colliding_objects)

        for index, colliding_object in enumerate(colliding_objects):

            if index == length:
                continue
            collider_aabb = aabbs[colliding_object]

            other_aabbs = [
                aabbs[other_object]
                for other_object in colliding_objects[index + 1 : length]
            ]

            collision_indices = collider_aabb.collidelistall(other_aabbs)
            candidates = [colliding_objects[i + index + 1] for i in collision_indices]
            candidate_colliders = [
                ColliderComponent.get(candidate) for candidate in candidates
            ]
            first_pass_candidates.update(
                {ColliderComponent.get(colliding_object): candidate_colliders}
            )

        return first_pass_candidates
