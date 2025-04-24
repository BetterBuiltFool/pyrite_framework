from __future__ import annotations

from typing import TypeAlias

from pygame import Vector2

Simplex: TypeAlias = list[Vector2, Vector2, Vector2]


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


def get_closest_edge(simplex: Simplex) -> tuple[Vector2, Vector2]:
    """
    Finds the verticies of the simplex defining the edge that's closests to the origin.

    :param simplex: A collection of vertices making a simplex
    :return: A tuple containing the two closests points to 0,0
    """
    sorted_simplex = sorted(simplex, key=Vector2.magnitude)
    return sorted_simplex[:2]


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


def get_unit_normal(start: Vector2, end: Vector2) -> Vector2:
    """
    Finds the normal 90 degrees clockwise (in display directions) between the two
    points, normalized.

    :param start: A Vector2 representing the starting position of the vector
    :param end: A Vector2 representing the end position of the vector
    :return: A Vector2 representing the normal direction of the vector, normalized
    """
    return get_normal(start, end).normalize()
