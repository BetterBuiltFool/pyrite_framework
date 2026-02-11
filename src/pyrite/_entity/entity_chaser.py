from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING

from pygame import Vector2

from pyrite._component.transform_component import TransformComponent
from pyrite._entity.entity import BaseEntity
import pyrite.time
from pyrite._types.protocols import (
    HasTransform,
    HasTransformProperty,
    HasTransformAttributes,
    HasTransformComponent,
    HasTransformComponentProperty,
)

if TYPE_CHECKING:

    from pygame.typing import Point


def invariant_dist(distance: float) -> float:
    return distance


class Chaser[TargetType](BaseEntity):
    """
    Base class for an entity that chases a target.
    """

    def __init__(
        self,
        enabled=True,
        transform: HasTransformAttributes | None = None,
        position: Point = (0, 0),
        target: TargetType | None = None,
        ease_factor: float = 8.0,
        max_distance: float = -1,
        dist_function: Callable[[float], float] | None = None,
    ) -> None:
        """
        Create an entity that will chase a target.

        :param enabled: Whether or not the entity is active, defaults to True
        :param transform: A transform or TransformComponent which the chaser will try
            to move towards the target, defaults to None
        :param position: Starting position, if no transform or TransformComponent is
            set, defaults to (0,0)
        :param target: An object that the Chaser will attempt to pursue, defaults to
            None
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

    @abstractmethod
    def _get_delta(self) -> Vector2:
        pass

    @abstractmethod
    def _update_position(self, delta: Vector2) -> None:
        pass

    def post_update(self) -> None:
        if not self.target:
            return
        delta = self.calculate_ease(self._get_delta())
        if self.max_distance >= 0:
            delta = self.clamp_magnitude(delta)
        self._update_position(delta)

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


class EntityChaser(Chaser[HasTransformComponent | HasTransformComponentProperty]):

    def _get_delta(self) -> Vector2:
        assert self.target
        return self.transform.world_position - self.target.transform.world_position

    def _update_position(self, delta: Vector2) -> None:
        assert self.target
        self.transform.world_position = self.target.transform.world_position + delta


class HasTransformChaser(Chaser[HasTransform | HasTransformProperty]):

    def _get_delta(self) -> Vector2:
        assert self.target
        return self.transform.world_position - self.target.transform.position

    def _update_position(self, delta: Vector2) -> None:
        assert self.target
        self.transform.world_position = self.target.transform.position + delta


class TransformChaser(Chaser[HasTransformAttributes]):

    def _get_delta(self) -> Vector2:
        assert self.target
        return self.transform.world_position - self.target.position

    def _update_position(self, delta: Vector2) -> None:
        assert self.target
        self.transform.world_position = self.target.position + delta
