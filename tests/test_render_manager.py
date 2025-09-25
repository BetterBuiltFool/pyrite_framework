from collections.abc import Callable, Sequence
from contextlib import contextmanager
from typing import Any
import unittest
from weakref import WeakSet

from pygame.rect import Rect as Rect

from pyrite._camera.camera import BaseCamera
from pyrite.core.render_system import (
    DefaultRenderManager,
    _get_draw_index,
)
from pyrite._entity.entity import BaseEntity
from pyrite.enum import Layer, RenderLayers
from pyrite.rendering import OrthoProjection, RectBounds
from pyrite._rendering.base_renderable import BaseRenderable
from pyrite._services.camera_service import CameraServiceProvider as CameraService
from pyrite._types.bounds import CullingBounds
from pyrite._types.camera import Camera
from pyrite._types.renderable import Renderable


class MockRenderable(BaseRenderable):

    def __init__(
        self,
        enabled=True,
        layer: Layer = RenderLayers.MIDGROUND,
        draw_index=-1,
    ) -> None:
        self._enabled = enabled
        self._layer = layer
        self.draw_index = draw_index

    def render(self, delta_time: float, camera: Camera):
        return super().render(delta_time, camera)

    def get_bounds(self) -> CullingBounds:
        return RectBounds(Rect(-1024, -1024, 2048, 2048))


class MockEntity(BaseEntity):

    pass


@contextmanager
def make_renderable(*args, **kwds):
    yield MockRenderable(*args, **kwds)


@contextmanager
def make_entity(*args, **kwds):
    yield MockEntity(*args, **kwds)


class TestDefaultRenderManager(unittest.TestCase):

    def assertIsSorted(
        self,
        sequence: Sequence[Any],
        key: Callable | None = None,
        ascending=True,
        msg: Any = None,
    ) -> None:
        if not ascending:
            sequence = list(reversed(sequence))
        if key is None:

            def default_key(item: Any) -> Any:
                return item

            key = default_key

        previous = None
        for item in sequence:
            if not previous:
                previous = item
                continue
            if msg is None:
                msg = f"Element {item} is out of order (element compared to {previous})"
            self.assertGreaterEqual(key(item), key(previous))

    def setUp(self) -> None:
        self.render_manager = DefaultRenderManager()

    def test_enable(self):
        # Ideal case
        with make_renderable(layer=RenderLayers.MIDGROUND) as renderable:
            self.assertNotIn(
                RenderLayers.MIDGROUND, self.render_manager.renderables.keys()
            )

            self.render_manager.enable(renderable)
            self.assertIn(
                RenderLayers.MIDGROUND, self.render_manager.renderables.keys()
            )

            self.assertIn(
                renderable,
                self.render_manager.renderables.get(RenderLayers.MIDGROUND, WeakSet()),
            )
            self.render_manager.renderables = {}

        # Renderable, no layer
        with make_renderable() as renderable:

            self.render_manager.enable(renderable)
            self.assertIn(
                RenderLayers.MIDGROUND, self.render_manager.renderables.keys()
            )
            self.assertIs(renderable.layer, RenderLayers.MIDGROUND)

            self.assertIn(
                renderable,
                self.render_manager.renderables.get(RenderLayers.MIDGROUND, WeakSet()),
            )
            self.render_manager.renderables = {}

    def test_disable(self):
        renderables = [MockRenderable() for _ in range(5)]

        for renderable in renderables:
            self.render_manager.enable(renderable)

        for renderable in renderables:
            self.assertIn(
                renderable,
                self.render_manager.renderables.get(RenderLayers.MIDGROUND, WeakSet()),
            )

        disabled_renderable = renderables[2]  # Arbitrary index

        self.render_manager.disable(disabled_renderable)

        for renderable in renderables:
            if renderable is disabled_renderable:
                continue
            self.assertIn(
                renderable,
                self.render_manager.renderables.get(RenderLayers.MIDGROUND, WeakSet()),
            )
        self.assertNotIn(
            disabled_renderable,
            self.render_manager.renderables.get(RenderLayers.MIDGROUND, WeakSet()),
        )

        # Try removing a renderable not in the collection
        self.render_manager.disable(disabled_renderable)

    def test_generate_render_queue(self):
        # Ideal case

        # Note: Doing these in one line breaks because they will all be the same object.
        backgrounds = []
        midgrounds = []
        foregrounds = []

        element_dict: dict[Layer, list[Renderable]] = {
            RenderLayers.BACKGROUND: backgrounds,
            RenderLayers.MIDGROUND: midgrounds,
            RenderLayers.FOREGROUND: foregrounds,
        }

        for layer, elements in element_dict.items():
            for i in range(3):
                elements.append(MockRenderable(layer=layer, draw_index=i))

        all_elements = [
            element for elements in element_dict.values() for element in elements
        ]
        for renderable in all_elements:
            self.render_manager.enable(renderable)

        default_camera = BaseCamera(OrthoProjection((0, 0, 100, 100)))
        CameraService._default_camera = default_camera

        render_queue = self.render_manager.generate_render_queue()
        self.maxDiff = None
        for layer, dict_elements in element_dict.items():
            render_elements = render_queue.get(layer, {})
            renderables = render_elements.get(default_camera, [])
            self.assertListEqual(dict_elements, renderables)

        self.render_manager.renderables = {}

        # Renderables out of order
        renderables: list[Renderable] = []
        element_dict: dict[Layer, list[Renderable]] = {
            RenderLayers.MIDGROUND: renderables
        }
        for layer, elements in element_dict.items():
            for i in range(3, 0, -1):
                new_element = MockRenderable(layer=layer, draw_index=i - 1)
                elements.append(new_element)
                self.render_manager.enable(new_element)

        render_queue = self.render_manager.generate_render_queue()
        render_elements = render_queue.get(RenderLayers.MIDGROUND, {})
        self.assertIsSorted(render_elements.get(default_camera, []), _get_draw_index)

        self.render_manager.renderables = {}

        # Extra layers
        renderables: list[Renderable] = []
        midgrounds: list[Renderable] = []
        extra_layer = Layer(-1)
        element_dict: dict[Layer, list[Renderable]] = {
            RenderLayers.MIDGROUND: midgrounds,
            extra_layer: renderables,
        }
        for layer, elements in element_dict.items():
            for i in range(3, 0, -1):
                new_element = MockRenderable(layer=layer, draw_index=i - 1)
                elements.append(new_element)
                self.render_manager.enable(new_element)

        render_queue = self.render_manager.generate_render_queue()

        self.assertIn(RenderLayers.MIDGROUND, render_queue.keys())
        self.assertNotIn(extra_layer, render_queue.keys())

        self.render_manager.renderables = {}


if __name__ == "__main__":

    unittest.main()
