from collections.abc import Callable, Sequence
from contextlib import contextmanager
import pathlib
import sys
from typing import Any
import unittest
from weakref import WeakSet

from pygame.rect import Rect as Rect
from pygame.surface import Surface as Surface
from pygame.typing import Point


sys.path.append(str(pathlib.Path.cwd()))

from src.pyrite.types.enums import Layer, RenderLayers  # noqa:E402
from src.pyrite._data_classes.renderer import (  # noqa:E402
    DefaultRenderer,
    _get_draw_index,
)
from src.pyrite.types.renderable import Renderable  # noqa:E402
from src.pyrite.types._base_type import _BaseType  # noqa:E402


class MockRenderable(Renderable):

    def __init__(
        self, game_instance=None, enabled=True, layer: Layer = None, draw_index=-1
    ) -> None:
        self.layer = layer
        self.draw_index = draw_index

    def render(self, delta_time: float) -> tuple[Surface, Point | Rect]:
        return super().render(delta_time)


class MockEntity(_BaseType):

    def __init__(self, game_instance=None, enabled=True) -> None:
        pass


@contextmanager
def make_renderable(*args, **kwds):
    yield MockRenderable(*args, **kwds)


@contextmanager
def make_entity(*args, **kwds):
    yield MockEntity(*args, **kwds)


class TestDefaultRenderer(unittest.TestCase):

    def assertIsSorted(
        self,
        sequence: Sequence[Any],
        key: Callable = None,
        ascending=True,
        msg: Any = None,
    ) -> None:
        if not ascending:
            sequence = reversed(sequence)
        if key is None:

            def key(item: Any) -> Any:
                return item

        previous = None
        for item in sequence:
            if not previous:
                previous = item
                continue
            if msg is None:
                msg = f"Element {item} is out of order (element compared to {previous})"
            self.assertGreaterEqual(key(item), key(previous))

    def setUp(self) -> None:
        self.renderer = DefaultRenderer()

    def test_enable(self):
        # Ideal case
        with make_renderable(layer=RenderLayers.MIDGROUND) as renderable:
            self.assertNotIn(RenderLayers.MIDGROUND, self.renderer.renderables.keys())

            self.renderer.enable(renderable)
            self.assertIn(RenderLayers.MIDGROUND, self.renderer.renderables.keys())

            self.assertIn(
                renderable,
                self.renderer.renderables.get(RenderLayers.MIDGROUND, WeakSet()),
            )
            self.renderer.renderables = {}

        # Renderable, no layer
        with make_renderable() as renderable:
            self.assertIs(renderable.layer, None)

            self.renderer.enable(renderable)
            self.assertIn(RenderLayers.MIDGROUND, self.renderer.renderables.keys())
            self.assertIs(renderable.layer, RenderLayers.MIDGROUND)

            self.assertIn(
                renderable,
                self.renderer.renderables.get(RenderLayers.MIDGROUND, WeakSet()),
            )
            self.renderer.renderables = {}

        # Not renderable
        with make_entity() as item:

            self.renderer.enable(item)

            self.assertNotIn(
                item,
                self.renderer.renderables.get(RenderLayers.MIDGROUND, WeakSet()),
            )
            self.renderer.renderables = {}

    def test_disable(self):
        renderables = [MockRenderable() for _ in range(5)]

        for renderable in renderables:
            self.renderer.enable(renderable)

        for renderable in renderables:
            self.assertIn(
                renderable,
                self.renderer.renderables.get(RenderLayers.MIDGROUND, WeakSet()),
            )

        disabled_renderable = renderables[2]  # Arbitrary index

        self.renderer.disable(disabled_renderable)

        for renderable in renderables:
            if renderable is disabled_renderable:
                continue
            self.assertIn(
                renderable,
                self.renderer.renderables.get(RenderLayers.MIDGROUND, WeakSet()),
            )
        self.assertNotIn(
            disabled_renderable,
            self.renderer.renderables.get(RenderLayers.MIDGROUND, WeakSet()),
        )

        # Try removing a mock entity
        entity = MockEntity()

        self.renderer.disable(entity)

        # Try removing a renderable not in the collection
        self.renderer.disable(disabled_renderable)

    def test_generate_render_queue(self):
        # Ideal case

        # Note: Doing these in one line breaks because they will all be the same object.
        backgrounds = []
        midgrounds = []
        foregrounds = []
        ui_elements = []

        element_dict: dict[Layer, list[Renderable]] = {
            RenderLayers.BACKGROUND: backgrounds,
            RenderLayers.MIDGROUND: midgrounds,
            RenderLayers.FOREGROUND: foregrounds,
            RenderLayers.UI_LAYER: ui_elements,
        }

        for layer, elements in element_dict.items():
            for i in range(3):
                elements.append(MockRenderable(layer=layer, draw_index=i))

        all_elements = [
            element for elements in element_dict.values() for element in elements
        ]
        for renderable in all_elements:
            self.renderer.enable(renderable)

        render_queue = self.renderer.generate_render_queue()
        self.maxDiff = None
        for layer, dict_elements in element_dict.items():
            render_elements = render_queue.get(layer, [])
            self.assertListEqual(dict_elements, render_elements)

        self.renderer.renderables = {}

        # Renderables out of order
        renderables: list[Renderable] = []
        element_dict: dict[Layer, list[Renderable]] = {
            RenderLayers.MIDGROUND: renderables
        }
        for layer, elements in element_dict.items():
            for i in range(3, 0, -1):
                new_element = MockRenderable(layer=layer, draw_index=i - 1)
                elements.append(new_element)
                self.renderer.enable(new_element)

        render_queue = self.renderer.generate_render_queue()
        self.assertIsSorted(render_queue.get(RenderLayers.MIDGROUND), _get_draw_index)

        self.renderer.renderables = {}

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
                self.renderer.enable(new_element)

        render_queue = self.renderer.generate_render_queue()

        self.assertIn(RenderLayers.MIDGROUND, render_queue.keys())
        self.assertNotIn(extra_layer, render_queue.keys())

        self.renderer.renderables = {}


if __name__ == "__main__":

    unittest.main()
