from __future__ import annotations
from typing import TYPE_CHECKING

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
    from pygame.typing import SequenceLike

    from pyrite._types.protocols import _HasCuboidAttribute
    from pyrite.cuboid import Cuboid

    Point3D = SequenceLike[float]
    CubeLike = (
        Cuboid | SequenceLike[float] | SequenceLike[Point3D] | _HasCuboidAttribute
    )

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
TransformLike = pyrite._types.protocols.TransformLike
