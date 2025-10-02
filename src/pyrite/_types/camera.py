from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING

# from pygame import Vector2

if TYPE_CHECKING:
    # from pygame.typing import Point
    from pyrite._types.view_bounds import CameraViewBounds
    from pyrite._types.renderable import Renderable
    from pyrite._types.projection import Projection
    from pyrite._types.protocols import RenderTarget
    from pyrite._rendering.viewport import Viewport
    from pyrite.enum import Layer
    from pyrite.events import OnEnable as EventOnEnable
    from pyrite.events import OnDisable as EventOnDisable
    from pyrite._transform.transform import Transform
    from pyrite._component.transform_component import TransformComponent


class Camera(ABC):
    """
    Defines the important attributes of a camera for the sake of drawing onto its
    surface.

    Can be constructed from the window.
    """

    layer_mask: Sequence[Layer]
    render_targets: Sequence[RenderTarget]
    projection: Projection
    transform: TransformComponent

    OnEnable: EventOnEnable
    OnDisable: EventOnDisable

    @property
    @abstractmethod
    def zoom_level(self) -> float:
        pass

    @zoom_level.setter
    @abstractmethod
    def zoom_level(self, zoom_level: float):
        pass

    @abstractmethod
    def refresh(self):
        """
        Returns the camera to a state that is ready for rendering.
        """
        pass

    @abstractmethod
    def cull(self, renderable: Renderable) -> bool:
        """
        Compares the bounds of the renderable to the camera's view bounds to determine
        if the renderable should be rendered.

        :param renderable: Any renderable item to be drawn.
        :return: True if the renderable is visible and should be drawn, otherwise False.
        """
        pass

    @abstractmethod
    def get_view_bounds(self) -> CameraViewBounds:
        """
        Gets the bounds object that represents the visible space of the camera.

        :return: A CameraViewBounds object describing the viewed space.
        """

    @abstractmethod
    def get_viewports(self) -> Sequence[Viewport]:
        """
        Gets a sequence of viewports targeted by the camera.

        :return: A sequence of viewports, empty if there are none.
        """
        pass

    @abstractmethod
    def render(self, render_target: RenderTarget):
        """
        Renders the camera view to the render target

        :param render_target: _description_
        """
        pass

    @abstractmethod
    def to_local(self, point: Transform) -> Transform:
        """
        Converts a point in world space to local space of the camera

        :param point: A transform, in world space
        :return: The local space equivalent of _point_
        """
        pass

    @abstractmethod
    def to_eye(self, point: Transform) -> Transform:
        """
        Converts a point in local space to the eye space of the camera, using the
        camera's projection.

        :param point: A transform, in local space of the camera
        :return: The eye space equivalent of _point_
        """

    @abstractmethod
    def to_world(self, point: Transform) -> Transform:
        """
        Converts a point in local space of the camera to world space.

        :param point: A transform, in local space
        :return: The world space equivalent of _point_
        """
        pass

    # @abstractmethod
    # def screen_to_world(self, point: Point, viewport_index: int = 0) -> Vector2:
    #     """
    #     Converts a screen coordinate into world coordinates.
    #     If the screen coordinate is outside the surface viewport, it will extrapolate
    #     to
    #     find the equivalent space.

    #     :param point: A location in screen space, usually pygame.mouse.get_pos()
    #     :param viewport_index: Index of the viewport to compare against, defaults to
    #     0.
    #     :raises IndexError: If the viewport_index is larger than the camera's
    #     number of render_targets.
    #     :return: The screen position, in world space relative to the camera
    #     """
    #     pass

    # @abstractmethod
    # def screen_to_world_clamped(
    #     self, point: Point, viewport_index: int = 0
    # ) -> Vector2 | None:
    #     """
    #     Variant of screen_to_world.
    #     Converts a screen coordinate into world coordinates.
    #     If the screen coordinate is outside the surface viewport, it will instead
    #     return
    #     None.

    #     Use this when it needs to be clear that the mouse is outside the camera
    #     view.

    #     :param point: A location in screen space, usually pygame.mouse.get_pos()
    #     :param viewport_index: Index of the viewport to compare against, defaults to
    #     0.
    #     :raises IndexError: If the viewport_index is larger than the camera's
    #     number of render_targets.
    #     :return: The screen position, in world space relative to the camera
    #     """
    #     pass
