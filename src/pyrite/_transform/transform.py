from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Vector2, Vector3
from pyglm import glm

from pyrite._types.protocols import HasTransformAttributes

if TYPE_CHECKING:
    from pygame.typing import Point
    from pyrite.types import Point3D


class Transform:

    def __init__(
        self, position: Point = (0, 0), rotation: float = 0, scale: Point = (1, 1)
    ) -> None:
        # self._position = Vector2(position)
        if len(position) < 3:
            position = position[0], position[1], 0
        if len(scale) < 3:
            scale = scale[0], scale[1], 1
        self._position = glm.vec3(position)
        self._rotation = glm.quat(glm.vec3(0, 0, glm.radians(rotation)))
        self._scale = glm.vec3(scale)

    @property
    def position(self) -> Vector2:
        """
        Represents the local position of the transform
        """
        return Vector2(self._position.xy)

    @position.setter
    def position(self, position: Point):
        if len(position) < 3:
            # Keep current z if a new one is not provided.
            position = position[0], position[1], self._position.z
        self._position = glm.vec3(position)

    @property
    def position_3d(self) -> Vector3:
        """
        Represents the local position of the transform.
        """
        return Vector3(self._position)

    @position_3d.setter
    def position_3d(self, position_3d: Point3D) -> None:
        # Skip the length check since we're assuming it's already a valid vec3 param
        self._position = glm.vec3(position_3d)

    @property
    def rotation(self) -> float:
        """
        Represents the local rotation of the transform
        """
        return glm.degrees(glm.eulerAngles(self._rotation).z)

    @rotation.setter
    def rotation(self, rotation: float):
        self._rotation = glm.quat(glm.vec3(0, 0, glm.radians(rotation)))

    @property
    def euler_angles(self) -> Vector3:
        return Vector3(glm.eulerAngles(self._rotation))

    @property
    def scale(self) -> Vector2:
        """
        Represents the local scaling of the transform
        """
        return Vector2(self._scale.xy)

    @scale.setter
    def scale(self, scale: Point):
        if len(scale) < 3:
            scale = scale[0], scale[1], 1
        self._scale = glm.vec3(scale)

    @property
    def scale_3d(self) -> Vector3:
        """
        Represents the local scaling of the transform
        """
        return Vector3(self._scale)

    @scale_3d.setter
    def scale_3d(self, scale_3d: Point3D):
        self._scale = glm.vec3(scale_3d)

    @property
    def matrix(self) -> glm.mat4x4:
        matrix = glm.translate(self._position) * glm.mat4(self._rotation)
        return glm.scale(matrix, self._scale)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, HasTransformAttributes):
            return False
        return (
            value.position == self.position
            and value.rotation == self.rotation
            and value.scale == self.scale
        )

    def copy(self) -> Transform:
        return Transform(self._position, self.rotation, self._scale)

    @staticmethod
    def generalize(
        branch: HasTransformAttributes, root: HasTransformAttributes
    ) -> Transform:
        """
        Applies a root transform to a local transform, converting it into the same
        relative space.

        Can also be done with the * operator.

        Can be stacked with other generalizations and localizations to convert from any
        reference frame to another.

        Inverse of Transform.localize()

        :Example:
        ```
        local_transform = Transform((5, 0), 0, (1, 1))
        root_transform = Transform((10, 10), 90, (2, 2))

        Transform.generalize(local_transform, root_transform) == Transform((10, 0), 90,
        (2, 2))
        ```

        _______________________________________________________________________________

        :param branch: A local transform-like object, being
        :param root: A transform-like object being treated like the new origin for the
            local transform.
        :return: A new transform, representing the current transform in the local space
            of _root_.
        """
        new_matrix = root.matrix * branch.matrix

        new_scale: glm.vec3 = glm.vec3()
        new_rotation: glm.quat = glm.quat()
        new_position: glm.vec3 = glm.vec3()
        skew: glm.vec3 = glm.vec3()
        perspective: glm.vec4 = glm.vec4()

        glm.decompose(
            new_matrix, new_scale, new_rotation, new_position, skew, perspective
        )
        new_transform = Transform()

        new_transform._position = new_position
        new_transform._rotation = new_rotation
        new_transform._scale = new_scale
        return new_transform

    def __mul__(self, other_transform: HasTransformAttributes) -> Transform:
        return Transform.generalize(other_transform, self)

    def __rmul__(self, other_transform: HasTransformAttributes) -> Transform:
        return Transform.generalize(self, other_transform)

    @staticmethod
    def localize(
        branch: HasTransformAttributes, root: HasTransformAttributes
    ) -> Transform:
        """
        Given two Transforms in the same relative space, finds the Transform local to
        the root that is equivalent of this Transform.

        Inverse of Transform.generalize()

        Can be stacked with other localizations and generalizations to convert from any
        reference frame to another.

        :Example:
        ```
        branch_transform = Transform((10, 0), 90, (2, 2))
        root_transform = Transform((10, 10), 90, (2, 2))

        Transform.localize(branch_transform, root_transform) == Transform((5, 0), 0, (1,
        1))
        ```

        _______________________________________________________________________________
        :param branch: A transform-like object to be made local to the _root_
        :param root: A transform-like object in the same space as the _branch_.
        :return: A new transform, equivalent to the difference between the current
            transform and _root_.
        """
        new_matrix = glm.inverse(root.matrix) * branch.matrix

        new_scale: glm.vec3 = glm.vec3()
        new_rotation: glm.quat = glm.quat()
        new_position: glm.vec3 = glm.vec3()
        skew: glm.vec3 = glm.vec3()
        perspective: glm.vec4 = glm.vec4()

        glm.decompose(
            new_matrix, new_scale, new_rotation, new_position, skew, perspective
        )
        new_transform = Transform()

        new_transform._position = new_position
        new_transform._rotation = new_rotation
        new_transform._scale = new_scale
        return new_transform

    def __truediv__(self, other: HasTransformAttributes) -> Transform:
        return Transform.localize(self, other)

    def __rtruediv__(self, other: HasTransformAttributes) -> Transform:
        return Transform.localize(other, self)

    def __repr__(self) -> str:
        return f"Transform({self.position}, {self.rotation}, {self.scale})"
