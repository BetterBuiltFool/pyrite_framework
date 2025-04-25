from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING, Any

from ..types import System
from .collider_component import ColliderComponent
from ..transform import TransformComponent
from .. import collider

from pygame import Vector2

if TYPE_CHECKING:
    from ..types.collider import Collider
    from ..transform import Transform
    from pygame import Rect

Simplex: TypeAlias = list[Vector2, Vector2, Vector2]


class ColliderSystem(System):

    def post_update(self, delta_time: float) -> None:
        colliding_objects = list(ColliderComponent.intersect(TransformComponent))

        first_pass_candidates = self.get_first_pass_collisions(  # noqa:F841
            colliding_objects
        )

    def get_first_pass_collisions(
        self, colliding_objects: list[Any]
    ) -> dict[ColliderComponent, list[ColliderComponent]]:
        first_pass_candidates: dict[ColliderComponent, list[ColliderComponent]] = {}

        aabbs = self.get_aabbs(colliding_objects)

        length = len(colliding_objects)

        for index, colliding_object in enumerate(colliding_objects):

            if index == length:
                continue

            other_candidates = colliding_objects[index + 1 : length]

            collider = ColliderComponent.get(colliding_object)

            for other_candidate in other_candidates:
                other_component = ColliderComponent.get(other_candidate)
                # Early break if masks don't interact
                if not (
                    collider.compare_mask(other_component)
                    or other_component.compare_mask(collider)
                ):
                    continue
                other_aabbs = aabbs[other_candidate]
                for aabb in aabbs[colliding_object]:
                    if not aabb.collidelist(other_aabbs):
                        # No interactions with the other's aabbs, so try the next
                        continue
                    # Found a hit, so add the candidates and break.
                    first_pass_candidates.setdefault(colliding_object, []).append(
                        other_candidate
                    )
                    break

        #     collider_aabb = aabbs[colliding_object]

        #     other_aabbs = [
        #         aabbs[other_object]
        #         for other_object in colliding_objects[index + 1 : length]
        #     ]

        #     collision_indices = collider_aabb.collidelistall(other_aabbs)
        #     candidates = [colliding_objects[i + index + 1] for i in collision_indices]
        #     candidate_colliders = [
        #         ColliderComponent.get(candidate) for candidate in candidates
        #     ]
        #     first_pass_candidates.update(
        #         {ColliderComponent.get(colliding_object): candidate_colliders}
        #     )

        return first_pass_candidates

    @staticmethod
    def get_aabbs(
        colliding_objects: list[Any],
    ) -> dict[Any, list[Rect]]:

        aabbs: dict[Any, list[Rect]] = {}

        for colliding_object in colliding_objects:
            component = ColliderComponent.get(colliding_object)
            world_transform = TransformComponent.get(colliding_object).world()
            aabb_list = aabbs.setdefault(colliding_object, [])
            for object_collider, transform in zip(
                component.get_colliders(), component.get_transforms()
            ):
                aabb_list.append(
                    object_collider.get_aabb(transform.generalize(world_transform))
                )

        return aabbs

    @staticmethod
    def support_function(
        direction: Vector2,
        collider_a: Collider,
        collider_b: Collider,
        transform_a: Transform,
        transform_b: Transform,
    ) -> Vector2:
        point_a = collider_a.get_furthest_vertex(direction, transform_a)
        point_b = collider_b.get_furthest_vertex(-direction, transform_b)

        return point_a - point_b

    @classmethod
    def collide(
        cls,
        collider_a: Collider,
        collider_b: Collider,
        transform_a: Transform,
        transform_b: Transform,
    ) -> bool:
        direction = Vector2(1, 0)  # Arbitrary direction

        # Get support point 1
        support_point = cls.support_function(
            direction, collider_a, collider_b, transform_a, transform_b
        )

        # Add to simplex
        simplex: Simplex = [support_point]

        # New direction through origin
        direction = -support_point

        # Get support point 2
        support_point = cls.support_function(
            direction, collider_a, collider_b, transform_a, transform_b
        )

        # Add to simplex
        simplex.append(support_point)

        # Short circuit if point is already invalid
        if support_point * direction < 0:
            return False

        # Loop
        while True:
            # Get the normal of the two closest points
            direction = collider.get_normal(simplex[0], simplex[1])

            # Get support point 3
            support_point = cls.support_function(
                direction, collider_a, collider_b, transform_a, transform_b
            )

            # Short circuit if point is already invalid
            if support_point * direction < 0:
                return False

            # Add to simplex
            simplex.append(support_point)

            # Simplex is now a triangle
            if collider.check_region(simplex):
                # Found our overlap!
                return True

            # Failed, reduce simplex and try again
            simplex = collider.get_closest_edge(simplex)
