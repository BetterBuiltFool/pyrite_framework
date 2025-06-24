"""
Pyrite module for drawing shapes directly to the screen, over a camera.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import pygame
from pygame import Rect

from .services import CameraService

if TYPE_CHECKING:
    from .camera import Camera
    from .rendering import Viewport
    from pygame.typing import ColorLike, Point


def rect(
    camera: Camera,
    viewport: Viewport,
    color: ColorLike,
    rect: Rect,
    width: int = 0,
    border_radius: int = -1,
    border_top_left_radius: int = -1,
    border_top_right_radius: int = -1,
    border_bottom_left_radius: int = -1,
    border_bottom_right_radius: int = -1,
) -> Rect:
    """
    Draws a rectangle over the screen, using a camera's view for reference.

    See pygame.draw.rect for details about parameters other that camera and viewport.

    :param camera: The camera whose view is being considered.
    :param viewport: The viewport being drawn to.

    :return: A Rectangle that surrounds the drawn area.
    """
    display = viewport.get_target_surface()

    # Remember that display is inverted compared to world
    screen_topleft = CameraService.world_to_screen(rect.bottomleft, camera, viewport)
    screen_bottomright = CameraService.world_to_screen(rect.topright, camera, viewport)

    rect_width = screen_bottomright[0] - screen_topleft[0]
    rect_height = screen_bottomright[1] - screen_topleft[1]
    draw_rect = Rect(*screen_topleft, rect_width, rect_height)

    return pygame.draw.rect(
        display,
        color,
        draw_rect,
        width,
        border_radius,
        border_top_left_radius,
        border_top_right_radius,
        border_bottom_left_radius,
        border_bottom_right_radius,
    )


def polygon(
    camera: Camera,
    viewport: Viewport,
    color: ColorLike,
    points: Sequence[Point],
    width: int = 0,
) -> Rect:
    """
    Draws a polgon over the screen, using a camera's view for reference.

    See pygame.draw.polygon for details about parameters other that camera and viewport.

    :param camera: The camera whose view is being considered.
    :param viewport: The viewport being drawn to.

    :return: A Rectangle that surrounds the drawn area.
    """
    display = viewport.get_target_surface()

    screen_points = [
        CameraService.world_to_screen(point, camera, viewport) for point in points
    ]

    return pygame.draw.polygon(display, color, screen_points, width)


def circle(
    camera: Camera,
    viewport: Viewport,
    color: ColorLike,
    center: Point,
    radius: int,
    width: int = 0,
    draw_top_right: bool = False,
    draw_top_left: bool = False,
    draw_bottom_left: bool = False,
    draw_bottom_right: bool = False,
) -> Rect:
    """
    Draws a circle over the screen, using a camera's view for reference.

    See pygame.draw.circle for details about parameters other that camera and viewport.

    :param camera: The camera whose view is being considered.
    :param viewport: The viewport being drawn to.

    :return: A Rectangle that surrounds the drawn area.
    """
    display = viewport.get_target_surface()

    screen_center = CameraService.world_to_screen(center, camera, viewport)

    return pygame.draw.circle(
        display,
        color,
        screen_center,
        radius,
        width,
        draw_top_right,
        draw_top_left,
        draw_bottom_left,
        draw_bottom_right,
    )


def aacircle(
    camera: Camera,
    viewport: Viewport,
    color: ColorLike,
    center: Point,
    radius: int,
    width: int = 0,
    draw_top_right: bool = False,
    draw_top_left: bool = False,
    draw_bottom_left: bool = False,
    draw_bottom_right: bool = False,
) -> Rect:
    """
    Draws an anti-aliased circle over the screen, using a camera's view for reference.

    See pygame.draw.aacircle for details about parameters other that camera and
    viewport.

    :param camera: The camera whose view is being considered.
    :param viewport: The viewport being drawn to.

    :return: A Rectangle that surrounds the drawn area.
    """
    display = viewport.get_target_surface()

    screen_center = CameraService.world_to_screen(center, camera, viewport)

    return pygame.draw.aacircle(
        display,
        color,
        screen_center,
        radius,
        width,
        draw_top_right,
        draw_top_left,
        draw_bottom_left,
        draw_bottom_right,
    )


def ellipse(
    camera: Camera,
    viewport: Viewport,
    color: ColorLike,
    rect: Rect,
    width: int = 0,
) -> Rect:
    """
    Draws an ellipse over the screen, using a camera's view for reference.

    See pygame.draw.ellipse for details about parameters other that camera and viewport.

    :param camera: The camera whose view is being considered.
    :param viewport: The viewport being drawn to.

    :return: A Rectangle that surrounds the drawn area.
    """
    display = viewport.get_target_surface()

    # Remember that display is inverted compared to world
    screen_topleft = CameraService.world_to_screen(rect.bottomleft, camera, viewport)
    screen_bottomright = CameraService.world_to_screen(rect.topright, camera, viewport)

    rect_width = screen_bottomright[0] - screen_topleft[0]
    rect_height = screen_bottomright[1] - screen_topleft[1]
    draw_rect = Rect(*screen_topleft, rect_width, rect_height)

    return pygame.draw.ellipse(
        display,
        color,
        draw_rect,
        width,
    )


def arc(
    camera: Camera,
    viewport: Viewport,
    color: ColorLike,
    rect: Rect,
    start_angle: float,
    stop_angle: float,
    width: int = 0,
) -> Rect:
    """
    Draws an arc over the screen, using a camera's view for reference.

    See pygame.draw.arc for details about parameters other that camera and viewport.

    :param camera: The camera whose view is being considered.
    :param viewport: The viewport being drawn to.

    :return: A Rectangle that surrounds the drawn area.
    """
    display = viewport.get_target_surface()

    # Remember that display is inverted compared to world
    screen_topleft = CameraService.world_to_screen(rect.bottomleft, camera, viewport)
    screen_bottomright = CameraService.world_to_screen(rect.topright, camera, viewport)

    rect_width = screen_bottomright[0] - screen_topleft[0]
    rect_height = screen_bottomright[1] - screen_topleft[1]
    draw_rect = Rect(*screen_topleft, rect_width, rect_height)

    return pygame.draw.arc(
        display,
        color,
        draw_rect,
        start_angle,
        stop_angle,
        width,
    )


def line(
    camera: Camera,
    viewport: Viewport,
    color: ColorLike,
    start_pos: Point,
    end_pos: Point,
    width: int = 1,
) -> Rect:
    """
    Draws a line over the screen, using a camera's view for reference.

    See pygame.draw.line for details about parameters other that camera and viewport.

    :param camera: The camera whose view is being considered.
    :param viewport: The viewport being drawn to.

    :return: A Rectangle that surrounds the drawn area.
    """
    display = viewport.get_target_surface()

    screen_start = CameraService.world_to_screen(start_pos, camera, viewport)
    screen_end = CameraService.world_to_screen(end_pos, camera, viewport)

    return pygame.draw.line(display, color, screen_start, screen_end, width)


def lines(
    camera: Camera,
    viewport: Viewport,
    color: ColorLike,
    closed: bool,
    points: Sequence[Point],
    width: int = 1,
) -> Rect:
    """
    Draws a series of lines over the screen, using a camera's view for reference.

    See pygame.draw.lines for details about parameters other that camera and viewport.

    :param camera: The camera whose view is being considered.
    :param viewport: The viewport being drawn to.

    :return: A Rectangle that surrounds the drawn area.
    """
    display = viewport.get_target_surface()

    screen_points = [
        CameraService.world_to_screen(point, camera, viewport) for point in points
    ]

    return pygame.draw.lines(display, color, closed, screen_points, width)


def aaline(
    camera: Camera,
    viewport: Viewport,
    color: ColorLike,
    start_pos: Point,
    end_pos: Point,
    width: int = 1,
) -> Rect:
    """
    Draws an anti-aliased line over the screen, using a camera's view for reference.

    See pygame.draw.aaline for details about parameters other that camera and viewport.

    :param camera: The camera whose view is being considered.
    :param viewport: The viewport being drawn to.

    :return: A Rectangle that surrounds the drawn area.
    """
    display = viewport.get_target_surface()

    screen_start = CameraService.world_to_screen(start_pos, camera, viewport)
    screen_end = CameraService.world_to_screen(end_pos, camera, viewport)

    return pygame.draw.aaline(display, color, screen_start, screen_end, width)


def aalines(
    camera: Camera,
    viewport: Viewport,
    color: ColorLike,
    closed: bool,
    points: Sequence[Point],
    width: int = 1,
) -> Rect:
    """
    Draws a series of anti-aliased lines over the screen, using a camera's view for
    reference.

    See pygame.draw.aalines for details about parameters other that camera and viewport.

    :param camera: The camera whose view is being considered.
    :param viewport: The viewport being drawn to.

    :return: A Rectangle that surrounds the drawn area.
    """
    display = viewport.get_target_surface()

    screen_points = [
        CameraService.world_to_screen(point, camera, viewport) for point in points
    ]

    return pygame.draw.aalines(display, color, closed, screen_points, width)
