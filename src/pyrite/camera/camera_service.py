from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

from pygame import Surface, Vector2, Vector3

from ..rendering.view_plane import ViewPlane
from ..rendering.rect_bounds import RectBounds

if TYPE_CHECKING:
    from .camera import Camera
    from ..types import CameraViewBounds, CullingBounds
    from pygame import Rect
    from pygame.typing import Point


class CameraService:

    _surfaces: WeakKeyDictionary[Camera, Surface] = WeakKeyDictionary()

    @classmethod
    def add_camera(cls, camera: Camera):
        """
        Adds the camera to the service.

        :param camera: The Camera object being added.
        """
        cls._rebuild_surface(camera)

    @classmethod
    def clear(cls, camera: Camera):
        surface = cls._surfaces.get(camera)
        surface.fill((0, 0, 0))

    @classmethod
    def get_bounds(cls, camera: Camera) -> CullingBounds:
        return RectBounds(cls.get_rect(camera))

    @classmethod
    def get_rect(cls, camera: Camera) -> Rect:
        surface = cls._surfaces.get(camera)
        return surface.get_rect()

    @classmethod
    def get_view_bounds(cls, camera: Camera) -> CameraViewBounds:
        return ViewPlane(cls._get_view_rect(camera))

    @classmethod
    def _get_view_rect(cls, camera: Camera) -> Rect:
        surface = cls._surfaces.get(camera)
        surface_rect = surface.get_rect().copy()
        surface_rect.center = camera.transform.world_position
        return surface_rect

    @classmethod
    def _get_projection_data(cls, camera: Camera) -> tuple[float, ...]:
        projection = camera.projection
        far_plane = projection.far_plane
        width, height = far_plane.size
        depth = projection.z_depth
        center_x, center_y = far_plane.center
        return width, height, depth, center_x, center_y

    @classmethod
    def local_to_ndc(cls, camera: Camera, local_coords: Vector3) -> Vector3:
        """
        Takes a point in local coordinates and transforms it into ndc space.

        :param clip_coords: A 3D point in the local space of the camera.
            For 2D, the Z axis is ignored.
        :return: A 3D point in standard ndc space.
        """
        # Frankly the only reason this is here is because the method will vary
        # depending on the renderer.
        # Default pyrite renderer doesn't use matrices, but openGL would, and I don't
        # want to have to overwrite the projection classes if it can be avoided.

        width, height, depth, center_x, center_y = cls._get_projection_data(camera)
        # Convert the local coords to projection space center.
        eye_point = (
            local_coords.x - center_x,
            local_coords.y - center_y,
            local_coords.z,
        )
        # Divide by projection size to normalize.
        ndc_coords = Vector3(
            eye_point[0] / (width / 2),
            eye_point[1] / (height / 2),
            eye_point[2] / (depth / 2),
        )
        return ndc_coords

    @classmethod
    def ndc_to_local(cls, camera: Camera, ndc_coords: Vector3) -> Vector3:
        """
        Takes a point in ndc space and transforms it into local coordinates

        :param ndc_coords: A 3D point in ndc space.
        :return: A 3D point in clip coordinates of the projection.
        """
        width, height, depth, center_x, center_y = cls._get_projection_data(camera)
        # Convert into projection space coords
        projection_coords = (
            int(ndc_coords[0] * (width / 2)),
            int(ndc_coords[1] * (height / 2)),
            int(ndc_coords[2] * (depth / 2)),
        )
        # Translate to local camera space.
        local_coords = Vector3(
            center_x + projection_coords[0],
            center_y + projection_coords[1],
            projection_coords[2],
        )
        return local_coords

    @classmethod
    def _rebuild_surface(cls, camera: Camera):
        # TODO Move this into CameraService
        zoom_factor = 1 / camera.zoom_level
        display_size = camera.projection.far_plane.size
        surface_size = (display_size[0] * zoom_factor), (display_size[1] * zoom_factor)
        surface = Surface(surface_size)
        cls._surfaces.update({camera: surface})

    @classmethod
    def to_local(cls, camera: Camera, point: Point) -> Point:
        # TODO Make this factor in the camera's TransformComponent
        return point - Vector2(cls._get_view_rect(camera).topleft)

    @classmethod
    def to_world(cls, camera: Camera, point: Point) -> Point:
        # TODO Make this factor in the camera's TransformComponent

        surface = cls._surfaces.get(camera)
        surface_rect = surface.get_rect().copy()
        surface_rect.center = camera.transform.world_position
        return point + Vector2(surface_rect.topleft)

    @classmethod
    def screen_to_world(
        cls, camera: Camera, point: Point, viewport_index: int = 0
    ) -> Point:
        # TODO Implement this
        # viewport = self.viewports[viewport_index]
        # viewport_rect = self._get_viewport_rect(viewport)

        # viewport_world = self.get_viewport_rect()

        # viewport_space_position = self._screen_to_viewport(
        #     point, viewport_rect, Vector2(viewport_world.size)
        # )

        # return viewport_space_position.elementwise() + viewport_world.topleft
        pass

    @classmethod
    def screen_to_world_clamped(
        cls, camera: Camera, point: Point, viewport_index: int = 0
    ) -> Point | None:
        # TODO Implement this
        # viewport = self.viewports[viewport_index]
        # viewport_rect = self._get_viewport_rect(viewport)

        # if not viewport_rect.collidepoint(point):
        #     return None

        # viewport_world = self.get_viewport_rect()

        # viewport_space_position = self._screen_to_viewport(
        #     point, viewport_rect, Vector2(viewport_world.size)
        # )

        # return viewport_space_position.elementwise() + viewport_world.topleft
        pass

    @classmethod
    def zoom(cls, camera: Camera, zoom: float):
        camera._zoom_level = zoom
        cls._rebuild_surface(camera)
