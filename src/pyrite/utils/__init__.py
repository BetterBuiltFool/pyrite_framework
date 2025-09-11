from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame.typing import Point


def point_to_tuple(point: Point) -> tuple[float, float]:
    return point[0], point[1]
