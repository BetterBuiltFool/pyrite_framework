from __future__ import annotations

from pygame import Rect, Vector2

from pyrite.transform.transform import Transform

from ..types.collider import Collider


class ElipseCollider(Collider):

    def __init__(self, radius: float) -> None:
        self.radius = radius

    def get_aabb(self, transform: Transform) -> Rect:
        diameter = self.radius * 2
        rect = Rect(0, 0, diameter * transform.scale.x, diameter * transform.scale.y)
        rect.center = transform.position
        return rect

    def collide(self, collide_with: Collider, delta_transform: Transform) -> bool:
        return super().collide(collide_with, delta_transform)

    def _gjk_support_function(self, vector: Vector2, transform: Transform) -> Vector2:
        return super()._gjk_support_function(vector, transform)
