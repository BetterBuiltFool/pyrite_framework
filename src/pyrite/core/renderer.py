from __future__ import annotations

from abc import ABC, abstractmethod
import bisect
from collections.abc import Sequence
from typing import Any, Self, TYPE_CHECKING
from weakref import WeakSet

# from pygame.typing import Point

from ..types.camera import CameraBase
from ..types.renderable import Renderable
from ..enum import RenderLayers

if TYPE_CHECKING:
    from ..camera import Camera
    from ..types._base_type import _BaseType
    from ..enum import Layer
    from pygame import Rect

import pygame


_active_render_manager: RenderManager = None


def get_render_manager() -> RenderManager:
    return _active_render_manager


def set_render_manager(manager: RenderManager):
    global _active_render_manager
    _active_render_manager = manager


_active_renderer: Renderer = None


def get_renderer() -> Renderer:
    return _active_renderer


def set_renderer(renderer: Renderer):
    global _active_renderer
    _active_renderer = renderer


_deferred_enables: set[Renderable] = set()


def enable(renderable: Renderable):

    if _active_render_manager:
        _active_render_manager.enable(renderable)
        return
    _deferred_enables.add(renderable)


def disable(renderable: Renderable):
    if _active_render_manager:
        _active_render_manager.disable(renderable)
        return
    _deferred_enables.discard(renderable)


class RenderManager(ABC):
    """
    An object for managing renderables. Can enable and disable them, and generates a
    render queue for the renderer.
    """

    def __new__(cls, *args, **kwds) -> Self:
        new_manager = super().__new__(cls)
        set_render_manager(new_manager)
        return new_manager

    def __init__(self) -> None:
        for renderable in _deferred_enables:
            self.enable(renderable)

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
    def enable(self, item: _BaseType) -> bool:
        """
        Adds a Renderable to the collection of renderables.

        Does nothing if the item is not a renderable.

        :param item: Object being enabled. Objects that are not renderable will be
        skipped.
        :return: True if enable is successful, False if not, such as object already
        enabled.
        """
        pass

    @abstractmethod
    def disable(self, item: _BaseType) -> bool:
        """
        Removes the item from the collection of renderables.

        :param item: Renderable being removed.
        :return: True if disable is successful, False if not, such as object already
        disabled.
        """
        pass

    @abstractmethod
    def get_number_renderables(self) -> int:
        """
        Returns the total number of renderables being tracked by the renderer.
        """
        pass

    @staticmethod
    def get_render_manager(**kwds) -> RenderManager:
        """
        Extracts a render manager from keyword arguments.
        Used for creating a render manager for a new Game instance
        """
        if (render_manager := kwds.get("render_manager", None)) is None:
            manager_type = get_default_render_manager_type()
            render_manager = manager_type()
        return render_manager


class Renderer(ABC):
    """
    Class responsible for drawing renderables to the screen.
    """

    def __new__(cls) -> Self:
        new_renderer = super().__new__(cls)
        set_renderer(new_renderer)
        return new_renderer

    @abstractmethod
    def render(
        self,
        window: pygame.Surface,
        delta_time: float,
        render_queue: dict[Any, Sequence[Renderable]],
    ):
        """
        Draws the items from the render queue onto the passed surface.

        :param window: The game window, receiving final draws
        :param render_queue: A list of items that need to be rendered to the surface.
        """
        pass

    @abstractmethod
    def get_rendered_last_frame(self) -> int:
        """
        Returns the number of rednerables that were actually drawn in the previous
        frame.
        """

    @staticmethod
    def get_renderer(**kwds) -> Renderer:
        """
        Extracts a renderer from keyword arguments.
        Used for creating a renderer for a new Game instance
        """
        if (renderer := kwds.get("renderer", None)) is None:
            renderer_type = get_default_renderer_type()
            renderer = renderer_type()
        return renderer


def _get_draw_index(renderable: Renderable) -> int:
    """
    Sort key for sorting by draw index.
    """
    return renderable.draw_index


class DefaultRenderManager(RenderManager):

    def __init__(self) -> None:
        self.renderables: dict[Layer, WeakSet[Renderable]] = {}
        self._rendered_last_frame: int = 0

        super().__init__()

    # Does not need a buffer for renderables, they should *NOT* be generated during the
    # render phase.

    def enable(self, item: _BaseType) -> bool:
        if not isinstance(item, Renderable):
            return False
        layer = item.layer
        if layer is None:
            # No layer set, force it to midground
            layer = RenderLayers.MIDGROUND
            item._layer = layer
        render_layer = self.renderables.setdefault(layer, WeakSet())

        # Check if this is a fresh enable
        newly_added = item not in render_layer

        render_layer.add(item)

        return newly_added

    def disable(self, item: _BaseType):
        if not isinstance(item, Renderable):
            return False
        layer = item.layer

        render_layer = self.renderables.get(layer, WeakSet())

        # Check if this is a fresh disable
        newly_disabled = item in render_layer

        if newly_disabled:
            # Changing this to check newly_disabled to avoid redundant check from
            # discard
            render_layer.remove(item)

        return newly_disabled

    def generate_render_queue(self) -> dict[Layer, Sequence[Renderable]]:
        render_queue: dict[Layer, Sequence[Renderable]] = {}
        cameras: set[CameraBase] = self.renderables.get(RenderLayers.CAMERA, {})

        for layer in RenderLayers._layers:
            layer_set = self.precull(self.renderables.get(layer, {}), layer, cameras)
            render_queue.update({layer: self.sort_layer(layer_set)})

        render_queue.update(
            {
                RenderLayers.UI_LAYER: self.sort_layer(
                    self.renderables.get(RenderLayers.UI_LAYER, {})
                )
            }
        )

        render_queue.update(
            {
                RenderLayers.CAMERA: self.sort_layer(
                    self.renderables.get(RenderLayers.CAMERA, {})
                )
            }
        )

        return render_queue

    def precull(
        self, layer_set: set[Renderable], layer: Layer, cameras: set[CameraBase] = None
    ) -> set[Renderable]:
        if not cameras:
            return layer_set
        culled_set: set[Renderable] = set()
        for camera in cameras:
            if layer in camera.layer_mask:
                continue
            culled_set |= set(camera.cull(layer_set))
        return culled_set

    def get_number_renderables(self) -> int:
        count = 0
        for layer_set in self.renderables.values():
            count += len(layer_set)
        return count

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


class DefaultRenderer(Renderer):

    def render_layer(
        self,
        layer_queue: Sequence[Renderable],
        cameras: Sequence[CameraBase],
        delta_time: float,
        layer: Layer,
    ):
        """
        Extracts the renderables from the layer_queue, and has them drawn to the
        cameras.

        :param layer_queue: The ordered sequence of renderables to be drawn.
        :param cameras: The cameras being drawn to.
        :param delta_time: Time passed since last frame.
        :param layer: the layer being drawn from, for layermask testing.
        """
        self._rendered_last_frame += len(layer_queue)
        for renderable in layer_queue:
            rendered_surface = renderable.render(delta_time)
            self.render_item(rendered_surface, renderable.get_rect(), cameras, layer)

    def render_item(
        self,
        rendered_surface: Renderable,
        renderable_rect: Rect,
        cameras: Sequence[CameraBase],
        layer: Layer,
    ):
        """
        Draws a renderable to the cameras, adjusting its world position to camera space.

        :param rendered_surface: The surface to be drawn to the camera.
        :param renderable_rect: The rendered item's rectangle in world space.
        :param cameras: The cameras being drawn to.
        :param layer: layer being drawn, for layermask testing.
        """
        for camera in cameras:
            if layer in camera.layer_mask:
                continue
            if not camera._in_view(renderable_rect):
                continue
            camera.surface.blit(
                rendered_surface, camera.to_local(renderable_rect.topleft)
            )

    def draw_camera(self, camera: Camera, window: pygame.Surface, delta_time: float):
        """
        Draws the given camera to the window, at each of its surface sectors.

        :param camera: Camera being drawn to the screen
        :param window: Game window being drawn to
        :param delta_time: Time passed since last frame, if needed for any calculations.
        """
        camera_surface = camera.render(delta_time)
        for sector in camera.surface_sectors:
            render_rect = sector.get_rect(window)
            window.blit(
                camera.scale_view(camera_surface, render_rect.size),
                render_rect,
            )

    def render_ui(
        self,
        ui_elements: Sequence[Renderable],
        window: pygame.Surface,
        delta_time: float,
    ):
        """
        Goes through the ui elements, and draws them to the screen. They are already in
        screen space, so they do not get adjusted.

        :param ui_elements: The sequence of ui elements to be drawn, in order.
        :param cameras: The cameras being drawn to.
        :param delta_time: Time passed since last frame.
        """
        for ui_element in ui_elements:
            surface = ui_element.render(delta_time)
            position = ui_element.get_rect().topleft
            window.blit(surface, position)

    def render(
        self,
        window: pygame.Surface,
        delta_time: float,
        render_queue: dict[Layer, Sequence[Renderable]],
    ):
        self._rendered_last_frame = 0
        cameras: tuple[CameraBase] = render_queue.get(RenderLayers.CAMERA, ())
        if not cameras:
            # Treat the screen as a camera for the sake of rendering if there are no
            # camera objects.
            cameras = (CameraBase(window),)  # Needs to be in a sequence

        for camera in cameras:
            camera.clear()

        for layer in RenderLayers._layers:
            # _layers is sorted by desired draw order.
            self.render_layer(render_queue.get(layer, []), cameras, delta_time, layer)

        # Render any cameras to the screen.
        for camera in render_queue.get(RenderLayers.CAMERA, ()):
            self.draw_camera(camera, window, delta_time)

        # Render the UI last.
        self.render_ui(render_queue.get(RenderLayers.UI_LAYER, []), window, delta_time)

    def get_rendered_last_frame(self) -> int:
        return self._rendered_last_frame


_default_render_manager_type = DefaultRenderManager


def get_default_render_manager_type() -> type[Renderer]:
    return _default_render_manager_type


def set_default_render_manager_type(render_manager_type: type[RenderManager]):
    global _default_render_manager_type
    _default_render_manager_type = render_manager_type


_default_renderer_type = DefaultRenderer


def get_default_renderer_type() -> type[Renderer]:
    return _default_renderer_type


def set_default_renderer_type(renderer_type: type[Renderer]):
    global _default_renderer_type
    _default_renderer_type = renderer_type
