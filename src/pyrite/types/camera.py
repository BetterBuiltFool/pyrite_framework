from abc import ABC
from collections.abc import Iterable


from src.pyrite.types.renderable import Renderable
from src.pyrite.types.enums import RenderLayers

import pygame


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
            position = self.viewport.topleft
        self.position = position

    def clear(self):
        self.surface.fill((0, 0, 0, 0))

    def cull(self, items: Iterable[Renderable]) -> Iterable[Renderable]:
        return items


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
        max_size = pygame.Rect(0, 0, *max_size)
        surface = pygame.Surface(max_size.size)
        CameraBase.__init__(self, surface, position)
        Renderable.__init__(
            self, game_instance, enabled, RenderLayers.CAMERA, draw_index
        )

    def clear(self):
        self.surface.fill((0, 0, 0, 255))

    def cull(self, items: Iterable[Renderable]) -> Iterable[Renderable]:
        return (item for item in items if self._in_view(item.get_rect()))

    def _in_view(self, rect: pygame.Rect) -> bool:
        return self.viewport.move(self.position).colliderect(rect)

    def get_rect(self) -> pygame.Rect:
        return self.viewport.move(self.position)

    def render(self, delta_time: float) -> tuple[pygame.Surface, pygame.typing.Point]:
        return (
            pygame.transform.scale(
                self.surface.subsurface(self.viewport), self.surface.get_rect().size
            ),
            (0, 0),
        )
