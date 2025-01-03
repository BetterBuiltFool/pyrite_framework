from __future__ import annotations


class Layer:

    def __init__(self, render_index: int = None) -> None:
        self._render_index = render_index

    @property
    def render_index(self) -> int:
        return self._render_index

    @render_index.setter
    def render_index(self, index: int):
        pass


class RenderLayers:
    background = Layer(0)
    midground = Layer(1)
    foreground = Layer(2)
    ui_layer = Layer(3)

    # Ordered set of layers
    _layers = [background, midground, foreground, ui_layer]

    @classmethod
    def add_layer(cls, layer: Layer):
        pass
