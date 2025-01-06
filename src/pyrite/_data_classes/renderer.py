from __future__ import annotations

from abc import ABC, abstractmethod
import bisect
from collections.abc import Sequence
from typing import Any, TYPE_CHECKING
from weakref import WeakSet

from src.pyrite.types.camera import CameraBase
from src.pyrite.types.renderable import Renderable
from src.pyrite.types.enums import RenderLayers

if TYPE_CHECKING:
    from src.pyrite.types._base_type import _BaseType
    from src.pyrite.game import Game
    from src.pyrite.types.enums import Layer

import pygame


class Renderer(ABC):
    """
    Class responsible to holding any enabled renderables,
    and drawing them to the screen.
    """

    def __init__(self, game_instance: Game) -> None:
        self.game_instance = game_instance

    @abstractmethod
    def generate_render_queue(self) -> dict[Any, Sequence[Renderable]]:
        """
        Generates a dict of renderables, in draw order.

        The keys are metadata used by the renderer to determine factors like layer
        culling and, partially, draw order. They can be of any type, but must be a type
        the render method knows how to handle.
        """
        pass

    @abstractmethod
    def render(
        self,
        window: pygame.Surface,
        delta_time: float,
        render_queue: dict[Any, Sequence[Renderable]],
    ):
        """
        Draws the items from the renderable dictionary onto the passed surface.

        :param window: The game window, receiving final draws
        :param render_queue: A list of items that need to be rendered to the surface.
        """
        pass

    @abstractmethod
    def enable(self, item: _BaseType):
        """
        Adds a Renderable to the collection of renderables.

        Does nothing if the item is not a renderable.

        :param item: Object being enabled. Objects that are not renderable will be
        skipped.
        """
        pass

    @abstractmethod
    def disable(self, item: _BaseType):
        """
        Removes the item from the collection of renderables.

        :param item: Renderable being removed.
        """
        pass

    @staticmethod
    def get_renderer(game_instance: Game, **kwds) -> Renderer:
        """
        Extracts a renderer from keyword arguments.
        Used for creating a renderer for a new Game instance
        """
        if (renderer := kwds.get("renderer", None)) is None:
            renderer = DefaultRenderer(game_instance)
        return renderer


def _get_draw_index(renderable: Renderable) -> int:
    """
    Sort key for sorting by draw index.
    """
    return renderable.draw_index


class DefaultRenderer(Renderer):
    """
    TODO Add cameras. Give a special layer that's always last.
    In the render phase, extract any cameras, draw to them, and then draw them to the
    screen (That's why they're last.)
    """

    def __init__(self, game_instance: Game) -> None:
        super().__init__(game_instance)
        self.renderables: dict[Layer, WeakSet[Renderable]] = {}

    def enable(self, item: _BaseType):
        if not isinstance(item, Renderable):
            return
        layer = item.layer
        if layer is None:
            # No layer set, force it to midground
            layer = RenderLayers.MIDGROUND
            item.layer = layer
        render_layer = self.renderables.setdefault(layer, WeakSet())
        render_layer.add(item)

    def disable(self, item: _BaseType):
        if not isinstance(item, Renderable):
            return
        layer = item.layer
        self.renderables.get(layer, WeakSet()).discard(item)

    def generate_render_queue(self) -> dict[Layer, Sequence[Renderable]]:
        render_queue: dict[Layer, Sequence[Renderable]] = {}
        cameras: set[CameraBase] = self.renderables.get(RenderLayers.CAMERA, {})

        for layer in RenderLayers._layers:
            layer_set = self.renderables.get(layer, {})
            culled_set: set[Renderable] = set()
            # Pre cull our renderables. This will reduce the amount of sorting to do.
            for camera in cameras:
                if layer in camera.layer_mask:
                    continue
                culled_set |= set(camera.cull(layer_set))
            # Puts everything into the renderqueue if there are no cameras
            layer_set = culled_set if cameras else layer_set
            render_queue.update({layer: self.sort_layer(layer_set)})

        render_queue.update(
            {
                RenderLayers.CAMERA: self.sort_layer(
                    self.renderables.get(RenderLayers.CAMERA, {})
                )
            }
        )

        return render_queue

    def render(
        self,
        window: pygame.Surface,
        delta_time: float,
        render_queue: dict[Layer, Sequence[Renderable]],
    ):
        cameras: tuple[CameraBase] = render_queue.get(RenderLayers.CAMERA, ())
        if not cameras:
            # Treat the screen as a camera for the sake of rendering if there are no
            # camera objects.
            cameras = (CameraBase(window),)  # Needs to be in a sequence

        for camera in cameras:
            camera.clear()

        for layer in RenderLayers._layers:
            # _layers is sorted by desired draw order.
            layer_queue = render_queue.get(layer, [])
            for camera in cameras:
                if layer in camera.layer_mask:
                    continue
                for renderable in layer_queue:
                    camera.draw(*renderable.render(delta_time))

        # Render any cameras to the screen.
        for camera in render_queue.get(RenderLayers.CAMERA, ()):
            camera_surface, camera_location = camera.render(delta_time)
            window.blit(
                pygame.transform.scale(camera_surface, window.get_rect().size),
                camera_location,
            )

    def sort_layer(self, renderables: Sequence[Renderable]) -> list[Renderable]:
        """
        Sorts a sequence of renderables by draw_index, such that they are ordered
        0 -> Infinity | -Infinity -> -1

        :param renderables: list of renderables to sort
        :return: Sorted list
        """
        renderables = sorted(renderables, key=_get_draw_index)
        pivot = bisect.bisect_left(renderables, 0, key=_get_draw_index)
        negatives = renderables[:pivot]
        del renderables[:pivot]

        negatives.reverse()

        return renderables + negatives
