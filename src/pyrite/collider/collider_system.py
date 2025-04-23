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

    vector_co = -simplex[2]

    normal_ac = ColliderSystem.get_normal(simplex[0], simplex[2])
    ac_dot = normal_ac.dot(vector_co)
    if ac_dot > 0:
        return False

    normal_cb = ColliderSystem.get_normal(simplex[2], simplex[1])
    cb_dot = normal_cb.dot(vector_co)
    if cb_dot > 0:
        return False
    return True


def get_closest_edge(simplex: Simplex) -> tuple[Vector2, Vector2]:
    sorted_simplex = sort(simplex)
    return sorted_simplex[:2]


def sort(simplex: Simplex) -> Simplex:
    return sorted(simplex, key=key)


def key(vector: Vector2) -> int:
    return vector.magnitude()


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
            direction = cls.get_normal(simplex[0], simplex[1])

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
            if check_region(simplex):
                # Found our overlap!
                return True

            # Failed, reduce simplex and try again
            simplex = get_closest_edge(simplex)

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
        edge = start - end
        return Vector2(edge.y, -edge.x).normalize()
