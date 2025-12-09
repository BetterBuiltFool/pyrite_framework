from __future__ import annotations

from typing import Any, TYPE_CHECKING, TypeGuard

from pygame import Rect


import pyrite._types.bounds
import pyrite._types.camera
import pyrite._types.component
import pyrite._types.debug_renderer
import pyrite._types.entity
import pyrite._types.projection
import pyrite._types.renderable
import pyrite._types.renderer
import pyrite._types.sprite
import pyrite._types.system
import pyrite._types.protocols
import pyrite._types.view_bounds

if TYPE_CHECKING:
    from pygame.typing import Point, RectLike, SequenceLike

    from pyrite._types.protocols import _HasCuboidAttribute
    from pyrite.cuboid import Cuboid

CullingBounds = pyrite._types.bounds.CullingBounds
Camera = pyrite._types.camera.Camera
Component = pyrite._types.component.Component
DebugRenderer = pyrite._types.debug_renderer.DebugRenderer
Entity = pyrite._types.entity.Entity
Projection = pyrite._types.projection.Projection
Renderable = pyrite._types.renderable.Renderable
Renderer = pyrite._types.renderer.Renderer
RendererProvider = pyrite._types.renderer.RendererProvider
Sprite = pyrite._types.sprite.Sprite
System = pyrite._types.system.System
CameraViewBounds = pyrite._types.view_bounds.CameraViewBounds

# Protocols
CanConstUpdate = pyrite._types.protocols.CanConstUpdate
CanPostUpdate = pyrite._types.protocols.CanPostUpdate
CanPreUpdate = pyrite._types.protocols.CanPreUpdate
CanUpdate = pyrite._types.protocols.CanUpdate
HasPosition = pyrite._types.protocols.HasPosition
HasTexture = pyrite._types.protocols.HasTexture
HasTransform = pyrite._types.protocols.HasTransform
HasTransformProperty = pyrite._types.protocols.HasTransformProperty
RenderTarget = pyrite._types.protocols.RenderTarget
HasTransformAttributes = pyrite._types.protocols.HasTransformAttributes

if TYPE_CHECKING:
    from pyglm import glm
    from pyrite._transform.transform import Transform

    Point3D = SequenceLike[float]

    type _SequenceBased = (
        SequenceLike[float]
        | SequenceLike[Point3D]
        | tuple[RectLike, Point]
        | tuple[RectLike, float, float]
    )

    type _CubeLikeNoAttribute = (Cuboid | _SequenceBased)

    type CubeLike = (_CubeLikeNoAttribute | _HasCuboidAttribute)
    RectPoint = tuple[RectLike, Point]
    RectBased = tuple[RectLike, float, float]

    CuboidTuple = tuple[float, float, float, float, float, float]

    Transform2DTuple = tuple[Point, float, Point]
    Transform3DPoints = tuple[Point3D, Point3D, Point3D]

    type _SequenceTransformLike = (Transform3DPoints | Transform2DTuple)

    type _HasTransformAccessible = HasTransform | HasTransformProperty

    type _TransformLikeNoAttribute = (
        Transform | _HasTransformAccessible | _SequenceTransformLike | glm.mat4x4
    )

    type TransformLike = (_TransformLikeNoAttribute | HasTransformAttributes)


# TODO Consider if these should be here or int the _types folder and imported to here.


def is_sequencelike(obj: Any) -> TypeGuard[SequenceLike]:
    if not hasattr(obj, "__len__"):
        return False
    if not hasattr(obj, "__getitem__"):
        return False

    return True


def has_cubelike_attribute(obj: Any) -> TypeGuard[_HasCuboidAttribute]:
    return hasattr(obj, "cuboid")


def is_sequence_based(obj: Any) -> TypeGuard[_SequenceBased]:
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__")


def is_number_sequence(obj: _SequenceBased) -> TypeGuard[SequenceLike[float]]:
    return all(isinstance(member, (int, float)) for member in obj)


def is_3d_points(obj: _SequenceBased) -> TypeGuard[SequenceLike[Point3D]]:
    return len(obj) == 2 and all(
        is_sequence_based(member) and len(member) == 3 for member in obj
    )


def has_rect_like(obj: _SequenceBased) -> TypeGuard[RectPoint | RectBased]:
    # I am NOT happy with this. I feel like there must be a better way to handle it.
    might_be_rect = obj[0]
    if not isinstance(might_be_rect, (int, float)):
        try:
            Rect(might_be_rect)
            return True
        except TypeError:
            pass
    return False


def has_transform(obj: Any) -> TypeGuard[_HasTransformAccessible]:
    return hasattr(obj, "transform")


def is_sequence_transformlike(obj: Any) -> TypeGuard[_SequenceTransformLike]:
    if not isinstance(obj, tuple):
        return False
    if len(obj) < 3:
        return False
    if not is_sequencelike(obj[0]):
        return False
    if not is_sequencelike(obj[2]):
        return False

    return True


def is_2d_transform(obj: _SequenceTransformLike) -> TypeGuard[Transform2DTuple]:
    return isinstance(obj[1], int | float)
