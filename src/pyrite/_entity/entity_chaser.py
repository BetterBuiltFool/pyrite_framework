from __future__ import annotations

from typing import TYPE_CHECKING

from pyrite._component.transform_component import TransformComponent
from pyrite._entity.entity import BaseEntity

if TYPE_CHECKING:
    from pyrite._types.protocols import (
        HasTransform,
        HasTransformProperty,
        TransformLike,
    )

    from pygame.typing import Point


class EntityChaser(BaseEntity):
    """
    An entity that will attempt to follow an object with a TransformComponent.
    """

    def __init__(
        self,
        enabled=True,
        transform: TransformLike | None = None,
        position: Point = (0, 0),
        target: HasTransform | HasTransformProperty | None = None,
        ease_factor: float = 8.0,
        max_distance: float = -1,
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
