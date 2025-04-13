from __future__ import annotations

from typing import Any, TYPE_CHECKING

from pygame import Vector2

from .transform import Transform
from . import transform_service

if TYPE_CHECKING:
    from pygame.typing import Point


class TransformComponent:

    def __init__(
        self,
        owner: Any,
        position: Point = (0, 0),
        rotation: float = 0,
        scale: Point = (1, 1),
    ) -> None:
        # super().__init__(position, rotation, scale)
        transform_service.initialize_component(
            self, Transform(position, rotation, scale)
        )
        self.owner = owner
        self._dirty = False

    @property
    def position(self) -> Vector2:
        return transform_service.get_local_position(self)

    @position.setter
    def position(self, new_position: Point):
        transform_service.set_local_position(self, new_position)

    @property
    def world_position(self) -> Vector2:
        """
        Gives the transform's position in world space.
        """
        return transform_service.get_world_position(self)

    @world_position.setter
    def world_position(self, new_position: Point):
        transform_service.set_world_position(self, new_position)

    @property
    def rotation(self) -> float:
        return transform_service.get_local_rotation(self)

    @rotation.setter
    def rotation(self, angle: float):
        transform_service.set_local_rotation(self, angle)

    @property
    def world_rotation(self) -> float:
        """
        Gives the transform's rotation in world space.
        """
        return transform_service.get_world_rotation(self)

    @world_rotation.setter
    def world_rotation(self, angle: float):
        transform_service.set_world_rotation(self, angle)

    @property
    def scale(self) -> Vector2:
        return transform_service.get_local_scale(self)

    @scale.setter
    def scale(self, new_scale: Point):
        transform_service.set_local_scale(self, new_scale)

    @property
    def world_scale(self) -> Vector2:
        """
        Gives the transform's scaling in world space.
        """
        return transform_service.get_world_scale(self)

    @world_scale.setter
    def world_scale(self, new_scale: Point):
        transform_service.set_world_scale(self, new_scale)

    def is_dirty(self) -> bool:
        return transform_service.is_dirty(self)

    def raw(self) -> Transform:
        """
        Returns a transform object representing this component in local space.
        """

        return transform_service.get_local(self)

    def world(self) -> Transform:
        """
        Returns a transform object representing this component in world space.
        """
        return transform_service.get_world(self)


def from_transform(owner: Any, transform: Transform) -> TransformComponent:
    """
    Create a transform component based on another transform.

    :param owner: The owner of the new transform.
    :param transform: The transform being copied
    :return: The newly-created transform component
    """
    # This can be overridden to return a subclass of TransformComponent, if needed.
    return TransformComponent(
        owner, transform._position, transform._rotation, transform._scale
    )


def from_attributes(
    owner: Any, position: Point = (0, 0), rotation: float = 0, scale: Point = (1, 1)
) -> TransformComponent:
    """
    Create a transform component from transform attributes.

    :param owner: The owner of the new transform.
    :param position: A Point in local space, defaults to (0, 0)
    :param rotation: An angle in degrees in local space, defaults to 0
    :param scale: A Point representing local scale , defaults to (1, 1)
    :return: The newly-created transform component
    """
    # This can be overridden to return a subclass of TransformComponent, if needed.
    return TransformComponent(owner, position, rotation, scale)
