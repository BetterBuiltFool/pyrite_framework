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
    ) -> tuple[Vector2, Vector2, Vector2]:
        """
        Determines the Minkowski difference between two colliders in the given
        direction.

        :param direction: A vector determining a direction to search for vertices.
        :param collider_a: The primary collider shape
        :param collider_b: The secondary collider shape
        :param transform_a: The transform value of the primary shape, in world space.
        :param transform_b: The transform value of the secondary shape, in world space.
        :return: A tuple containing:

            - A point relative the the origin, as part of a simplex.

            - The furthest vertex of _collider_a_, in world space.

            - The furthest vertex of _collider_b_, in world space.
        """
        point_a = collider_a.get_furthest_vertex(direction, transform_a)
        point_b = collider_b.get_furthest_vertex(-direction, transform_b)

        return point_a - point_b, point_a, point_b

    @staticmethod
    def collide(
        collider_a: Shape,
        collider_b: Shape,
        transform_a: Transform,
        transform_b: Transform,
    ) -> tuple[bool, Simplex]:
        """
        Runs the Gilbert-Johnson-Keerthi algorithm over the two shapes to determine if
        they overlap.

        :param collider_a: The primary collider shape
        :param collider_b: The secondary collider shape
        :param transform_a: The transform value of the primary shape, in world space.
        :param transform_b: The transform value of the secondary shape, in world space.
        :return: True is an overlap is detected, otherwise False. In either case, the
            resultant simplex.
        """
        direction = Vector2(1, 0)  # Arbitrary direction

        # Get support point 1
        support_point, *_ = GJKFunctions.support_function(
            direction, collider_a, collider_b, transform_a, transform_b
        )

        # Add to simplex
        simplex: Simplex = [support_point]

        # New direction through origin
        direction = -support_point

        # Get support point 2
        support_point, *_ = GJKFunctions.support_function(
            direction, collider_a, collider_b, transform_a, transform_b
        )

        # Add to simplex
        simplex.append(support_point)

        # Short circuit if point is already invalid
        if support_point * direction < 0:
            return False, simplex

        # Loop

        # Capping at 16 iterations.
        # There's a hard (for me) to diagnose bug which can cause infinite looping.
        # Frankly, 16 iterations should be more than enough. Any more than that and
        # we're talking about very slight overlap.

        # I _think_ this issue is cause by two ellipses just barely touching, causing
        # the simplex triangle to get smaller and smaller but never quite breaking the
        # bounds. I _think_ given enough time, it would eventually resolve, but I can't
        # tell for sure.
        # Ellipses and Stadia technically have infinite vertices on their curves, and
        # would be the cause of this.

        # Still, *not* worth fixing.

        for _ in range(16):
            # Get the normal of the two closest points
            direction = GJKFunctions.get_normal(simplex[0], simplex[1])

            # Get support point 3
            support_point, point_a, point_b = GJKFunctions.support_function(
                direction, collider_a, collider_b, transform_a, transform_b
            )

            # Short circuit if point is already invalid
            if support_point * direction < simplex[0] * direction:
                break

            # Add to simplex
            simplex.append(support_point)

            # Simplex is now a triangle
            if GJKFunctions.check_region(simplex):
                # Found our overlap!
                return True, simplex

            # Failed, reduce simplex and try again
            simplex = GJKFunctions.get_closest_edge(simplex)
        return False, simplex


_default_collider_functions: type[GJKFunctions] = GJKFunctions


def get_collider_functions() -> type[GJKFunctions]:
    """
    Returns the current set of functions necessary for doing collision detection.
    Between this and set_collider_functions, actual method of detecting collisions is
    customizable.
    """
    return _default_collider_functions


def set_collider_functions(collider_functions: type[GJKFunctions]):
    """
    Sets the object for useful collider functions.

    Call this before creating the instance of the ColliderSystem.

    :param collider_functions: A subtype of GJKFunctions, as a class
    """
    global _default_collider_functions
    _default_collider_functions = collider_functions
