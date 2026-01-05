from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Vector2, Vector3

import glm

from pyrite._types.protocols import HasTransformAttributes

from pyrite.types import (
    is_sequence_transformlike,
    is_2d_transform,
    has_transform,
)

if TYPE_CHECKING:
    from pygame.typing import Point
    from pyrite.types import (
        Point3D,
        TransformLike,
        _TransformLikeNoAttribute,
        _HasTransformAccessible,
    )


BAD_TRANSFORMLIKE_EXCEPTION = TypeError("Expected Transform-style object")


class Transform:

    def __init__(
        self,
        position: glm.vec3 = glm.vec3(),
        rotation: glm.quat = glm.quat(),
        scale: glm.vec3 = glm.vec3(1, 1, 1),
    ) -> None:
        self._position = position
        self._rotation = rotation
        self._scale = scale

    @property
    def position(self) -> Vector2:
        """
        Represents the local position of the transform
        """
        return Vector2(self._position.x, self._position.y)

    @position.setter
    def position(self, position: Point):
        if len(position) < 3:
            # Keep current z if a new one is not provided.
            position = position[0], position[1], self._position.z
        self._position = glm.vec3(*position)

    @property
    def position_3d(self) -> Vector3:
        """
        Represents the local position of the transform.
        """
        return Vector3(self._position)

    @position_3d.setter
    def position_3d(self, position_3d: Point3D) -> None:
        # Skip the length check since we're assuming it's already a valid vec3 param
        self._position = glm.vec3(*position_3d)

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
        return Vector2(self._scale.x, self._scale.y)

    @scale.setter
    def scale(self, scale: Point):
        if len(scale) < 3:
            scale = scale[0], scale[1], 1
        self._scale = glm.vec3(*scale)

    @property
    def scale_3d(self) -> Vector3:
        """
        Represents the local scaling of the transform
        """
        return Vector3(self._scale)

    @scale_3d.setter
    def scale_3d(self, scale_3d: Point3D):
        self._scale = glm.vec3(*scale_3d)

    @property
    def matrix(self) -> glm.mat4x4:
        matrix = glm.translate(self._position) * glm.mat4_cast(self._rotation)
        return glm.scale(matrix, self._scale)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, HasTransformAttributes):
            return False
        return (
            value.position == self.position
            and value.rotation == self.rotation
            and value.scale == self.scale
        )

    @staticmethod
    def _extract_transformlike_from_attribute(
        has_transformlike_attribute: _HasTransformAccessible,
    ) -> _TransformLikeNoAttribute:
        """
        Takes an object with a `transform` attribute and extracts the transformlike
        value from it. Calls recursively if needed.

        :param has_transformlike_attribute: An object with a cuboid attribute, as
            defined by the _HasTransformAccessible protocol.
        :return: A TransformLike object that isn't _TransformLikeNoAttribute.
        """
        transformlike = has_transformlike_attribute.transform
        if callable(transformlike):
            transformlike = transformlike()
        if has_transform(transformlike):
            # Recursive check, incase somehow we end up with a multi-layer-deep
            # nest of _HasTransformAccessible.
            # Worth note that this will be a problem if the nesting is infinite,
            # of course.
            transformlike = Transform._extract_transformlike_from_attribute(
                transformlike
            )

        # Currently in python 3.12, so TypeIs is not available, and TypeGuard isn't
        # smart enough to determine that there can no longer be a
        # _HasTransformAccessible.
        # Need to use type:ignore to get around this.
        # TODO: Update python and switch to TypeIs
        return transformlike  # type:ignore

    def copy(self) -> Transform:
        return Transform(self._position, self._rotation, self._scale)

    @staticmethod
    def generalize(
        branch: HasTransformAttributes, root: HasTransformAttributes
    ) -> glm.mat4x4:
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
        return root.matrix * branch.matrix

    def __mul__(
        self, other_transform: HasTransformAttributes | glm.mat4x4
    ) -> glm.mat4x4:
        if isinstance(other_transform, glm.mat4x4):
            return self.matrix * other_transform
        return Transform.generalize(other_transform, self)

    def __rmul__(
        self, other_transform: HasTransformAttributes | glm.mat4x4
    ) -> glm.mat4x4:
        if isinstance(other_transform, glm.mat4x4):
            return other_transform * self.matrix
        return Transform.generalize(self, other_transform)

    @staticmethod
    def localize(
        branch: HasTransformAttributes, root: HasTransformAttributes
    ) -> glm.mat4x4:
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
        return glm.inverse(root.matrix) * branch.matrix

    def __truediv__(self, other: HasTransformAttributes | glm.mat4x4) -> glm.mat4x4:
        if isinstance(other, glm.mat4x4):
            return glm.inverse(self.matrix) * other
        return Transform.localize(self, other)

    def __rtruediv__(self, other: HasTransformAttributes | glm.mat4x4) -> glm.mat4x4:
        if isinstance(other, glm.mat4x4):
            return glm.inverse(other) * self.matrix
        return Transform.localize(other, self)

    def __repr__(self) -> str:
        return f"Transform({self.position}, {self.rotation}, {self.scale})"

    @staticmethod
    def new(transformlike: TransformLike) -> Transform:
        """
        Creates a new Transform from any TransformLike value.

        Note: If you know the subtype of your TransformLike, it will always be faster
        to create it directly with the appropriate method.

        :param transformlike: Any TransformLike value.
        :raises BAD_TRANSFORMLIKE_EXCEPTION: If a transform cannot be constructed from
            the given value.
        :return: A new Transform.
        """
        if has_transform(transformlike):
            transformlike = Transform._extract_transformlike_from_attribute(
                transformlike
            )
        if isinstance(transformlike, Transform):
            return Transform.from_transform(transformlike)
        elif isinstance(transformlike, HasTransformAttributes):
            return Transform.from_matrix(transformlike.matrix)
        elif isinstance(transformlike, glm.mat4x4):
            return Transform.from_matrix(transformlike)
        elif is_sequence_transformlike(transformlike):
            if is_2d_transform(transformlike):
                return Transform.from_2d(*transformlike)
            else:
                # transformlike must be type Transform3DPoints by now
                # TODO upgrade Python and make TypeGuards to TypeIs
                return Transform.from_euler_rotation(*transformlike)  # type:ignore

        raise BAD_TRANSFORMLIKE_EXCEPTION

    @staticmethod
    def from_transform(
        transformlike: Transform,
    ) -> Transform:
        """
        Creates a new Transform from an existing Transform.

        :param transformlike: A Transform object
        :return: A duplicate of transformlike
        """
        return Transform(
            transformlike._position, transformlike._rotation, transformlike._scale
        )

    @staticmethod
    def from_2d(
        position: Point = (0, 0), rotation: float = 0, scale: Point | float = 1
    ) -> Transform:
        """
        Creates a new Transform from a sequence of 2D transform data.

        3D info is filled with default values.

        :param position: A point in space, must be at least 2D, defaults to (0, 0)
        :param rotation: Rotation along the z-axis, in degrees, defaults to 0
        :param scale: A tuple describing the scale of the Transform, either as a tuple,
            or as a single number for uniform scaling, defaults to 1
        :return: A new transform with the provided parameters.
        """
        if len(position) < 3:
            position = (position[0], position[1], 0)
        if isinstance(scale, float | int):
            scale = (scale, scale, scale)
        if len(scale) < 3:
            scale = (scale[0], scale[1], 1)
        return Transform(
            glm.vec3(*position),
            glm.quat(glm.vec3(0, 0, glm.radians(rotation))),
            glm.vec3(*scale),
        )

    @staticmethod
    def from_euler_rotation(
        position: Point3D, rotation: Point3D, scale: Point3D | float = 1
    ) -> Transform:
        """
        Creates a new Transform from 3D data, using Euler numbers for rotation.

        :param position: A point in 3D space.
        :param rotation: Rotation, defined by yaw, pitch, and roll, in degrees.
        :param scale: A tuple describing the scale of the Transform, either as a tuple,
            or as a single number for uniform scaling, defaults to 1
        :return: A new transform with the provided parameters.
        """
        if isinstance(scale, float | int):
            scale = (scale, scale, scale)
        return Transform(
            glm.vec3(*position),
            glm.quat(glm.radians(glm.vec3(*rotation))),
            glm.vec3(*scale),
        )

    @staticmethod
    def from_matrix(matrix: glm.mat4x4) -> Transform:
        """
        Creates a new Transform from a 4x4 affine matrix.

        :param matrix: A 4x4 affine matrix.
        :return: A new Transform, from which to_matrix should match the input matrix.
        """
        scale: glm.vec3 = glm.vec3()
        rotation: glm.quat = glm.quat()
        position: glm.vec3 = glm.vec3()
        skew: glm.vec3 = glm.vec3()
        perspective: glm.vec4 = glm.vec4()

        # glm not recognizing the typing properly, but this does run as expecter
        # so, it gets ignored.
        glm.decompose(
            matrix, scale, rotation, position, skew, perspective  # type:ignore
        )

        return Transform(position, rotation, scale)
