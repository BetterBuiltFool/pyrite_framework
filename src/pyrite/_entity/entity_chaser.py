from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from pygame import Vector2

from pyrite._component.transform_component import TransformComponent
from pyrite._entity.entity import BaseEntity
import pyrite.time

if TYPE_CHECKING:
    from pyrite._types.protocols import (
        HasTransformComponent,
        HasTransformComponentProperty,
        HasTransformAttributes,
    )

    from pygame.typing import Point


def invariant_dist(distance: float) -> float:
    return distance


class EntityChaser(BaseEntity):
    """
    An entity that will attempt to follow an object with a TransformComponent.
    """

    def __init__(
        self,
        enabled=True,
        transform: HasTransformAttributes | None = None,
        position: Point = (0, 0),
        target: HasTransformComponent | HasTransformComponentProperty | None = None,
        ease_factor: float = 8.0,
        max_distance: float = -1,
        dist_function: Callable[[float], float] | None = None,
    ) -> None:
        """
        Create an EntityChaser with the following properties:

        :param enabled: Whether or not the entity is active, defaults to True
        :param transform: A transform or TransformComponent which the chaser will try
            to move towards the target, defaults to None
        :param position: Starting position, if no transform or TransformComponent is
            set, defaults to (0,0)
        :param target: An object with a TransformComponent, which the chaser will try
            to follow, defaults to None
        :param ease_factor: Determines the rate at which the camera pursues the target.
        Larger = slower, defaults to 8.0
        :param max_distance: Maximum distance, in world space, that the chaser may be
            from its target. If negative, this behavior is disabled, defaults to -1
        """
        super().__init__(enabled)
        if transform is not None:
            if isinstance(transform, TransformComponent):
                # If we're being passed something else's transform,
                # we'll just use that instead.
                self.transform = transform
            else:
                self.transform = TransformComponent.from_transform(self, transform)
        else:
            self.transform = TransformComponent.from_attributes(self, position)
        self.target = target
        self.ease_factor = ease_factor
        self.max_distance = max_distance

        if not dist_function:
            dist_function = invariant_dist

        self.dist_function = dist_function

    def post_update(self) -> None:
        if not self.target:
            return
        delta = self.calculate_ease(
            self.transform.world_position - self.target.transform.world_position
        )
        if self.max_distance >= 0:
            delta = self.clamp_magnitude(delta)
        self.transform.world_position = self.target.transform.world_position + delta

    def calculate_ease(self, delta: Vector2) -> Vector2:
        distance = delta.magnitude()
        if distance == 0:
            return delta
        delta_normalized = delta.normalize()
        distance_adjustment = distance / self.ease_factor
        distance_adjustment *= 60 * pyrite.time.delta_time()
        distance -= distance_adjustment

        return delta_normalized * distance

    def clamp_magnitude(self, delta: Vector2) -> Vector2:
        return delta.clamp_magnitude(0, self.dist_function(self.max_distance))

    def stop(self) -> None:
        """
        Clears all references and disables self.
        """

        # If there's a set dist function, it may contain a reference, so we reset it so
        # we can clean up properly.
        self.dist_function = invariant_dist

        self.enabled = False
