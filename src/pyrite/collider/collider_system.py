from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING, Any

from ..types import System
from .collider_component import ColliderComponent
from ..transform import TransformComponent
from .. import collider

from pygame import Vector2

if TYPE_CHECKING:
    from pygame import Rect

Simplex: TypeAlias = list[Vector2, Vector2, Vector2]


class ColliderSystem(System):

    def post_update(self, delta_time: float) -> None:
        colliding_objects = list(ColliderComponent.intersect(TransformComponent))

        # Should be the fastest way of flushing all the buffers once and only once
        map(ColliderComponent._flush_buffer, colliding_objects)

        first_pass_candidates = self.get_first_pass_collisions(  # noqa:F841
            colliding_objects
        )

        for collider_component, candidates in first_pass_candidates.items():
            for candidate in candidates:
                pass
                if not (self.collide_between(collider_component, candidate)):
                    continue
                # Update the collision lists
                if collider_component.compare_mask(candidate):
                    # colldier_component can touch candidate
                    if collider_component.add_collision(candidate):
                        collider_component.OnTouch(collider_component, candidate)
                    collider_component.WhileTouching(collider_component, candidate)

                if candidate.compare_mask(collider_component):
                    # candidate can touch collider_component
                    if candidate.add_collision(collider_component):
                        candidate.OnTouch(candidate, collider_component)
                    candidate.WhileTouching(candidate, collider_component)

    @classmethod
    def get_first_pass_collisions(
        cls, colliding_objects: list[Any]
    ) -> dict[ColliderComponent, list[ColliderComponent]]:
        first_pass_candidates: dict[ColliderComponent, list[ColliderComponent]] = {}

        aabbs = cls.get_aabbs(colliding_objects)

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
                    if aabb.collidelist(other_aabbs) < 0:
                        # No interactions with the other's aabbs, so try the next
                        continue
                    # Found a hit, so add the candidates and break.
                    first_pass_candidates.setdefault(collider, []).append(
                        other_component
                    )
                    break

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

    @classmethod
    def collide_between(
        cls, component_a: ColliderComponent, component_b: ColliderComponent
    ) -> bool:
        """
        Determines if there is overlap with _other_collider_

        :param other_component: Another collider component that is a potential overlap.
        :return: True if the components have any overlapping colliders.
        """
        this_transform = TransformComponent.get(component_a.owner)
        other_transform = TransformComponent.get(component_b.owner)
        return any(
            collider.collide(
                collider_a,
                collider_b,
                this_transform * transform_a,
                other_transform * transform_b,
            )
            for collider_b, transform_b in zip(
                component_b.get_colliders(), component_b.get_transforms()
            )
            for collider_a, transform_a in zip(
                component_a.get_colliders(), component_a.get_transforms()
            )
        )
