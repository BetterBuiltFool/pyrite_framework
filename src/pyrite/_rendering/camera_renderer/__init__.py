from __future__ import annotations

from typing import TYPE_CHECKING

from pyrite._rendering.camera_renderer.camera_renderer import (
    CameraRenderer,
    DefaultCameraRenderer,
)
from pyrite._types.camera import CameraBase as Camera
from pyrite._types.renderer import RendererProvider

if TYPE_CHECKING:
    from pyrite._types.protocols import RenderTarget


class CameraRendererProvider(RendererProvider[CameraRenderer]):

    _renderer: CameraRenderer = DefaultCameraRenderer()

    @classmethod
    def hotswap(cls, renderer: CameraRenderer):
        cls._renderer = renderer

    @classmethod
    def render(cls, delta_time: float, renderable: Camera, target: RenderTarget):
        cls._renderer.render(delta_time, renderable, target)

    @classmethod
    def get_smooth_scale(cls) -> bool:
        return cls._renderer.smooth_scale

    @classmethod
    def set_smooth_scale(cls, smooth: bool = True):
        cls._renderer.smooth_scale = smooth
