from __future__ import annotations
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types import Container


_default_container_getter = None


def get_default_container() -> Container | None:
    return _default_container_getter()


def set_default_container_type(getter: Callable):
    """
    Sets the variable that is called by get_default_container.

    :param getter: A callable that returns a container or None.
    """
    global _default_container_getter
    _default_container_getter = getter
