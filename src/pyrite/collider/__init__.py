from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING

from pygame import Vector2

if TYPE_CHECKING:
    from ..types.shape import Shape
    from ..transform import Transform


Simplex: TypeAlias = list[Vector2, Vector2, Vector2]


class GJKFunctions:

    @staticmethod
    def check_region(simplex: Simplex) -> bool:
        """
        Determines of the origin is located within the triangular simplex.


        :param simplex: A simplex containing three verticies
        :return: True if the origin is contained, False otherwise.
        """
        vector_ao = -simplex[0]
        edge_ab = simplex[1] - simplex[0]
        ab_pos = edge_ab.dot(vector_ao) > 0

        vector_bo = -simplex[1]
        edge_bc = simplex[2] - simplex[1]
        bc_pos = edge_bc.dot(vector_bo) > 0

        if ab_pos != bc_pos:
            return False

        vector_co = -simplex[2]
        edge_ca = simplex[0] - simplex[2]
        ca_pos = edge_ca.dot(vector_co) > 0

        return ca_pos == ab_pos

    @staticmethod
    def get_closest_edge(simplex: Simplex) -> tuple[Vector2, Vector2]:
        """
        Finds the verticies of the simplex defining the edge that's closests to the
        origin.

        :param simplex: A collection of vertices making a simplex
        :return: A tuple containing the two closests points to 0,0
        """
        sorted_simplex = sorted(simplex, key=Vector2.magnitude)
        return sorted_simplex[:2]

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
        return edge.rotate(-90)

    @staticmethod
    def get_unit_normal(start: Vector2, end: Vector2) -> Vector2:
        """
        Finds the normal 90 degrees clockwise (in display directions) between the two
        points, normalized.

        :param start: A Vector2 representing the starting position of the vector
        :param end: A Vector2 representing the end position of the vector
        :return: A Vector2 representing the normal direction of the vector, normalized
        """
        return GJKFunctions.get_normal(start, end).normalize()

    @staticmethod
    def support_function(
        direction: Vector2,
        collider_a: Shape,
        collider_b: Shape,
        transform_a: Transform,
        transform_b: Transform,
    ) -> Vector2:
        point_a = collider_a.get_furthest_vertex(direction, transform_a)
        point_b = collider_b.get_furthest_vertex(-direction, transform_b)

        return point_a - point_b

    @staticmethod
    def collide(
        collider_a: Shape,
        collider_b: Shape,
        transform_a: Transform,
        transform_b: Transform,
    ) -> bool:
        direction = Vector2(1, 0)  # Arbitrary direction

        # Get support point 1
        support_point = GJKFunctions.support_function(
            direction, collider_a, collider_b, transform_a, transform_b
        )

        # Add to simplex
        simplex: Simplex = [support_point]

        # New direction through origin
        direction = -support_point

        # Get support point 2
        support_point = GJKFunctions.support_function(
            direction, collider_a, collider_b, transform_a, transform_b
        )

        # Add to simplex
        simplex.append(support_point)

        # Short circuit if point is already invalid
        if support_point * direction < 0:
            return False

        # Loop
        # while True:

        # Capping at 16 iterations.
        # There's a hard (for me) to diagnose bug which can cause infinite looping.
        # Frankly, 16 iterations should be more than enough. Any more than that and
        # we're talking about very slight overlap.

        for _ in range(16):
            # Get the normal of the two closest points
            direction = GJKFunctions.get_normal(simplex[0], simplex[1])

            # Get support point 3
            support_point = GJKFunctions.support_function(
                direction, collider_a, collider_b, transform_a, transform_b
            )

            # Short circuit if point is already invalid
            if support_point * direction < 0:
                return False

            # Add to simplex
            simplex.append(support_point)

            # Simplex is now a triangle
            if GJKFunctions.check_region(simplex):
                # Found our overlap!
                return True

            # Failed, reduce simplex and try again
            simplex = GJKFunctions.get_closest_edge(simplex)


def get_collider_functions() -> type[GJKFunctions]:
    return GJKFunctions
