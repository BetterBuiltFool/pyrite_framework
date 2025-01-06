from abc import ABC
from collections.abc import Iterable


from src.pyrite.types.renderable import Renderable
from src.pyrite.types.enums import RenderLayers

import pygame
from pygame import Vector2


class CameraBase(ABC):
    """
    Defines the important attributes of a camera for the sake of drawing onto its
    surface.

    Can be constructed from the window.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        position: pygame.typing.Point = None,
    ) -> None:
        self.surface = surface
        self.viewport = surface.get_rect()
        """
        A rectangle representing the actual viewable area of the camera
        """
        if position is None:
            position = self.viewport.center
        self.position = Vector2(position)

    def clear(self):
        self.surface.fill((0, 0, 0, 0))

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            Vector2(self.get_surface_rect().topleft) + Vector2(self.viewport.topleft),
            self.viewport.size,
        )
        # return self.viewport.move(-Vector2(self.get_surface_rect().topleft))

    def get_surface_rect(self) -> pygame.Rect:
        return self.surface.get_rect(center=self.position)

    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        self.surface.blit(
            surface,
            self.to_local(rect.topleft),
        )

    def cull(self, items: Iterable[Renderable]) -> Iterable[Renderable]:
        return (item for item in items if self._in_view(item.get_rect()))

    def _in_view(self, rect: pygame.Rect) -> bool:
        return self.get_rect().colliderect(rect)

    def to_local(self, point: pygame.typing.Point) -> Vector2:
        point = Vector2(point)

        return point - Vector2(self.get_surface_rect().topleft)

    def to_world(self, point: pygame.typing.Point) -> Vector2:
        point = Vector2(point)

        return point + Vector2(self.get_surface_rect().topleft)


class Camera(CameraBase, Renderable):
    """
    Basic form of a camera that is capable of rendering to the screen.
    """

    def __init__(
        self,
        max_size: pygame.typing.Point,
        position: pygame.typing.Point = None,
        game_instance=None,
        enabled=True,
        draw_index=0,
    ) -> None:
        self.max_size = Vector2(max_size)
        surface = pygame.Surface(self.max_size)
        CameraBase.__init__(self, surface, position)
        Renderable.__init__(
            self, game_instance, enabled, RenderLayers.CAMERA, draw_index
        )

    def clear(self):
        self.surface.fill((0, 0, 0, 255))

    def render(self, delta_time: float) -> tuple[pygame.Surface, pygame.typing.Point]:
        return (
            self.surface.subsurface(self.viewport),
            (0, 0),
        )

    def zoom(self, zoom_level: float):
        if zoom_level < 1:
            raise ValueError("Cannot zoom out beyond zoom_level 1")
        center = self.viewport.center
        self.viewport.size = self.max_size / zoom_level
        self.viewport.center = center
