from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING, Any

from ..types import System
from .collider_component import ColliderComponent
from ..transform import TransformComponent

from pygame import Vector2, Vector3

if TYPE_CHECKING:
    from ..types.collider import Collider
    from ..transform import Transform

Simplex: TypeAlias = list[Vector2, Vector2, Vector2]


def check_region(simplex: Simplex) -> bool:
    vector_a_c = simplex[0] - simplex[2]
    vector_b_c = simplex[1] - simplex[2]
    vector_c_o = -simplex[2]
    triple_a_c = triple_product(vector_b_c, vector_a_c, vector_a_c)
    triple_b_c = triple_product(vector_a_c, vector_b_c, vector_b_c)

    if triple_a_c.dot(vector_c_o) > 0:
        return False
    if triple_b_c.dot(vector_c_o) > 0:
        return False
    return True


def get_closest_edge(simplex: Simplex) -> tuple[Vector2, Vector2]:
    return sort(simplex)[:2]


def sort(simplex: Simplex) -> Simplex:
    return sorted(simplex, key=key)


def key(vector: Vector2) -> int:
    return len(vector)


def triple_product(vector_a: Vector2, vector_b: Vector2, vector_c: Vector2) -> Vector2:
    vector_a3 = Vector3(*vector_a, 0)
    vector_b3 = Vector3(*vector_b, 0)
    vector_c3 = Vector3(*vector_c, 0)
    product = (vector_a3 * vector_b3) * vector_c3
    return product.xy


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
        direction = Vector2(1, 0)
        sp1 = cls.support_function(
            direction, collider_a, collider_b, transform_a, transform_b
        )
        direction = -sp1
        sp2 = cls.support_function(
            direction, collider_a, collider_b, transform_a, transform_b
        )
        direction = cls.get_normal(sp1, sp2)
        sp3 = cls.support_function(
            direction, collider_a, collider_b, transform_a, transform_b
        )
        simplex = [sp1, sp2, sp3]
        if check_region(simplex):
            return True
        p1, p2 = get_closest_edge(simplex)
        direction = cls.get_normal(p1, p2)
        sp4 = cls.support_function(
            direction, collider_a, collider_b, transform_a, transform_b
        )
        simplex = [p1, p2, sp4]
        return check_region(simplex)

    @staticmethod
    def get_normal(start: Vector2, end: Vector2) -> Vector2:
        """
        Finds the normal 90 degrees clockwise (in display directions) between the two
        points

        :param start: A Vector2 representing the starting position of the vector
        :param end: A Vector2 representing the end position of the vector
        :return: A Vector2 representing the normal direction of the vector
        """
        # Creates a normal 90 degrees clockwise from from the origin
        edge = end - start
        return Vector2(-edge.y, edge.x).normalize()
