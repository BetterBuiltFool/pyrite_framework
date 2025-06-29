from __future__ import annotations

from typing import Any, TYPE_CHECKING

from pygame import Vector2

from ..component import Component
from .transform import Transform
from ..services import TransformService
from ..types import TransformLike


if TYPE_CHECKING:
    from pygame.typing import Point


class TransformComponent(Component):

    def __init__(
        self,
        owner: Any,
        position: Point = (0, 0),
        rotation: float = 0,
        scale: Point = (1, 1),
    ) -> None:
        super().__init__(owner)
        TransformService.initialize_component(
            self, Transform(position, rotation, scale)
        )
        self._dirty = False

    @property
    def position(self) -> Vector2:
        """
        :return: Position in local space
        """
        return TransformService.get_local_position(self)

    @position.setter
    def position(self, new_position: Point):
        TransformService.set_local_position(self, new_position)

    @property
    def world_position(self) -> Vector2:
        """
        :return: Position in world space.
        """
        return TransformService.get_world_position(self)

    @world_position.setter
    def world_position(self, new_position: Point):
        TransformService.set_world_position(self, new_position)

    @property
    def rotation(self) -> float:
        """
        :return: Rotation in local space, in degrees.
        """
        return TransformService.get_local_rotation(self)

    @rotation.setter
    def rotation(self, angle: float):
        TransformService.set_local_rotation(self, angle)

    @property
    def world_rotation(self) -> float:
        """
        :Return: Rotation in world space, in degrees.
        """
        return TransformService.get_world_rotation(self)

    @world_rotation.setter
    def world_rotation(self, angle: float):
        TransformService.set_world_rotation(self, angle)

    @property
    def scale(self) -> Vector2:
        """
        :return: Local scaling factor.
        """
        return TransformService.get_local_scale(self)

    @scale.setter
    def scale(self, new_scale: Point):
        TransformService.set_local_scale(self, new_scale)

    @property
    def world_scale(self) -> Vector2:
        """
        :return: World scaling factor.
        """
        return TransformService.get_world_scale(self)

    @world_scale.setter
    def world_scale(self, new_scale: Point):
        TransformService.set_world_scale(self, new_scale)

    def is_dirty(self) -> bool:
        """
        :return: True if the component is in need of updates.
        """
        return TransformService.is_dirty(self)

    def raw(self) -> Transform:
        """
        Returns a transform object representing this component in local space.
        """

        return TransformService.get_local(self)

    def world(self) -> Transform:
        """
        Returns a transform object representing this component in world space.
        """
        return TransformService.get_world(self)

    def __str__(self) -> str:
        return f"Local: {self.raw()}, World: {self.world()}"


def from_transform(owner: Any, transform: TransformLike) -> TransformComponent:
    """
    Create a transform component based on another transform.

    :param owner: The owner of the new transform.
    :param transform: The transform being copied
    :return: The newly-created transform component
    """
    # This can be overridden to return a subclass of TransformComponent, if needed.
    return TransformComponent(
        owner, transform.position, transform.rotation, transform.scale
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
