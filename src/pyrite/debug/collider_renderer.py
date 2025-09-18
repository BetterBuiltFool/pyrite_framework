from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame import Color
import pymunk

from pyrite._types.debug_renderer import DebugRenderer
from .. import draw
from ..physics import RigidbodyComponent

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from pygame.typing import ColorLike, Point
    from ..core.render_system import RenderQueue
    from ..types import Camera


class ColliderRenderer(DebugRenderer):

    def __init__(self, draw_color: ColorLike) -> None:
        self.color = Color(draw_color)
        self.font = pygame.font.Font()

    def draw_circle(self, cameras: Iterable[Camera], position: Point, radius: float):
        for camera in cameras:
            for viewport in camera.get_viewports():
                draw.circle(
                    camera,
                    viewport,
                    self.color,
                    position,
                    int((radius / 2) * camera.zoom_level),
                    width=1,
                )

    def draw_poly(
        self, cameras: Iterable[Camera], position: Point, points: Sequence[Point]
    ):
        points = [(position[0] + point[0], position[1] + point[1]) for point in points]
        for camera in cameras:
            for viewport in camera.get_viewports():
                draw.polygon(camera, viewport, self.color, points, width=1)

    def draw_to_screen(self, cameras: Iterable[Camera], render_queue: RenderQueue):

        for component in RigidbodyComponent.get_instances().values():
            pos = component.body.position
            for shape in component.body.shapes:
                match shape.__class__:
                    case pymunk.shapes.Circle:
                        assert isinstance(shape, pymunk.shapes.Circle)
                        self.draw_circle(cameras, pos + shape.offset, shape.radius)
                    case pymunk.shapes.Poly:
                        assert isinstance(shape, pymunk.shapes.Poly)
                        self.draw_poly(cameras, pos, shape.get_vertices())

        # for layer in RenderLayers._layers:
        #     layer_dict = render_queue.get(layer, {})
        #     for renderables in layer_dict.values():
        #         for renderable in renderables:
        #             bounds = renderable.get_bounds()
        #             bounds_rect = bounds.get_rect()
        #             for camera in cameras:
        #                 for viewport in camera.get_viewports():
        #                     draw.rect(
        #                         camera,
        #                         viewport,
        #                         self.color,
        #                         bounds_rect,
        #                         width=1,
        #                     )
