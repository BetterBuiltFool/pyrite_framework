from __future__ import annotations

from typing import TYPE_CHECKING

from .camera_renderer import CameraRenderer, DefaultCameraRenderer
from ...types import Camera, RendererProvider
from ...types.render_target import RenderTarget

if TYPE_CHECKING:
    pass


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
