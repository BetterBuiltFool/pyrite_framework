from __future__ import annotations

from typing import Any, TYPE_CHECKING

from pygame import Vector2

if TYPE_CHECKING:
    from pygame.typing import Point


class Transform:

    def __init__(
        self, position: Point = (0, 0), rotation: float = 0, scale: Point = (1, 1)
    ) -> None:
        self._position = Vector2(position)
        self._rotation = rotation
        self._scale = Vector2(scale)

    @property
    def position(self) -> Vector2:
        """
        Represents the local position of the transform
        """
        return self._position

    @position.setter
    def position(self, new_position: Point):
        self._position = Vector2(new_position)

    @property
    def rotation(self) -> float:
        """
        Represents the local rotation of the transform
        """
        return self._rotation

    @rotation.setter
    def rotation(self, angle: float):
        self._rotation = angle

    @property
    def scale(self) -> Vector2:
        """
        Represents the local scaling of the transform
        """
        return self._scale

    @scale.setter
    def scale(self, new_scale: Point):
        self._scale = Vector2(new_scale)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Transform):
            # Only a Transform or subclass can be equal.
            # If it's not even a Transform, why bother comparing further?
            return False
        return (
            value._position == self._position
            and value._rotation == self._rotation
            and value._scale == self._scale
        )


class TransformComponent(Transform):

    def __init__(
        self,
        owner: Any,
        position: Point = (0, 0),
        rotation: float = 0,
        scale: Point = (1, 1),
    ) -> None:
        super().__init__(position, rotation, scale)
        self.owner = owner
        self._dirty = False

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, new_position: Point):
        self._dirty = True
        self._position = Vector2(new_position)

    def get_world_position(self) -> Vector2:
        """
        Gives the transform's position in world space.

        TODO Make this calculate the world space, currently is just local.
        """
        return self._position

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, angle: float):
        self._dirty = True
        self._rotation = angle

    def get_world_rotation(self) -> float:
        """
        Gives the transform's rotation in world space.

        TODO Make this calculate the world space, currently is just local.
        """
        return self._rotation

    @property
    def scale(self) -> Vector2:
        return self._scale

    @scale.setter
    def scale(self, new_scale: Point):
        self._dirty = True
        self._scale = Vector2(new_scale)

    def get_world_scale(self) -> Vector2:
        """
        Gives the transform's scaling in world space.

        TODO Make this calculate the world space, currently is just local.
        """
        return self._scale

    def raw(self) -> Transform:
        """
        Returns a base transform equal to this WorldTransform
        """

        return Transform(self._position, self._rotation, self._scale)


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
