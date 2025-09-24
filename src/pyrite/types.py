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

    Point3D = SequenceLike[float]

CullingBounds = pyrite._types.bounds.CullingBounds
Camera = pyrite._types.camera.CameraBase
Component = pyrite._types.component.Component
DebugRenderer = pyrite._types.debug_renderer.DebugRenderer
Entity = pyrite._types.entity.Entity
Projection = pyrite._types.projection.Projection
Renderable = pyrite._types.renderable.Renderable
Renderer = pyrite._types.renderer.Renderer
RendererProvider = pyrite._types.renderer.RendererProvider
Sprite = pyrite._types.sprite.BaseSprite
System = pyrite._types.system.System
# TransformLike = pyrite._types.transform.TransformLike
CameraViewBounds = pyrite._types.view_bounds.CameraViewBounds
