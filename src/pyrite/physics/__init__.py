from __future__ import annotations

from typing import Any, TYPE_CHECKING
from weakref import WeakValueDictionary

import cffi

from .collider_component import ColliderComponent

if TYPE_CHECKING:
    from pymunk import Arbiter, Body

# Calculating the system's max int value for setting the collision type of
# ColliderComponents
COMPONENT_TYPE: int = 2 ** (cffi.FFI().sizeof("int") * 8 - 1) - 1
_bodies: WeakValueDictionary[Body, Any] = WeakValueDictionary()


def get_collider_components(
    arbiter: Arbiter,
) -> tuple[ColliderComponent, ColliderComponent]:
    shape1, shape2 = arbiter.shapes
    body1 = shape1.body
    body2 = shape2.body
    owner1 = _bodies.get(body1)
    owner2 = _bodies.get(body2)
    return ColliderComponent.get(owner1), ColliderComponent.get(owner2)
