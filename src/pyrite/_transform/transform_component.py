from __future__ import annotations

from typing import Any, TYPE_CHECKING

from pygame import Vector2

from pyrite._component.component import BaseComponent as Component
from pyrite._transform.transform import Transform
from pyrite._services.transform_service import (
    TransformServiceProvider as TransformService,
)
from pyrite._types.protocols import TransformLike


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
        return TransformService.get_local(self).position

    @position.setter
    def position(self, position: Point):
        local = TransformService.get_local(self)
        local.position = position
        TransformService.set_local(self, local)
        TransformService.make_dirty(self)

    @property
    def world_position(self) -> Vector2:
        """
        :return: Position in world space.
        """
        return TransformService.get_world(self).position

    @world_position.setter
    def world_position(self, position: Point):
        world = TransformService.get_world(self)
        world.position = position
        TransformService.set_world(self, world)
        TransformService.make_dirty(self)

    @property
    def rotation(self) -> float:
        """
        :return: Rotation in local space, in degrees.
        """
        return TransformService.get_local(self).rotation

    @rotation.setter
    def rotation(self, rotation: float):
        local = TransformService.get_local(self)
        local.rotation = rotation
        TransformService.set_local(self, local)
        TransformService.make_dirty(self)

    @property
    def world_rotation(self) -> float:
        """
        :Return: Rotation in world space, in degrees.
        """
        return TransformService.get_world(self).rotation

    @world_rotation.setter
    def world_rotation(self, rotation: float):
        world = TransformService.get_world(self)
        world.rotation = rotation
        TransformService.set_world(self, world)
        TransformService.make_dirty(self)

    @property
    def scale(self) -> Vector2:
        """
        :return: Local scaling factor.
        """
        return TransformService.get_local(self).scale

    @scale.setter
    def scale(self, scale: Point):
        local = TransformService.get_local(self)
        local.scale = scale
        TransformService.set_local(self, local)
        TransformService.make_dirty(self)

    @property
    def world_scale(self) -> Vector2:
        """
        :return: World scaling factor.
        """
        return TransformService.get_world(self).scale

    @world_scale.setter
    def world_scale(self, scale: Point):
        world = TransformService.get_world(self)
        world.scale = scale
        TransformService.set_world(self, world)

    def is_dirty(self) -> bool:
        """
        :return: True if the component is in need of updates.
        """
        return TransformService.is_dirty(self)

    def has_changed(self) -> bool:
        """
        :return: True if the component has been changed in the last frame.
        """
        return TransformService.has_changed(self)

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

    @staticmethod
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

    @staticmethod
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
