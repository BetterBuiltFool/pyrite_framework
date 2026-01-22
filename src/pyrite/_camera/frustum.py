from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Frustum:
    """
    Truncated pyramid shape used for perspective camera volumes.

    :param fov_y: Angle of view along the y-axis, in radians.
    :param aspect_ratio: Ratio between height and width of the bases of the frustum.
    :param z_near: Distance from the angle where the near base is established.
    :param z_far: Distance from the angle where the far base is established.
    """

    fov_y: float
    aspect_ratio: float
    z_near: float
    z_far: float
