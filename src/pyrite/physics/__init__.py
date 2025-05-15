from __future__ import annotations

from typing import Any, TYPE_CHECKING
from weakref import WeakValueDictionary

import cffi

if TYPE_CHECKING:
    from pymunk import Body

# Calculating the system's max int value for setting the collision type of
# ColliderComponents
COMPONENT_TYPE: int = 2 ** (cffi.FFI().sizeof("int") * 8 - 1) - 1
_bodies: WeakValueDictionary[Body, Any] = WeakValueDictionary()
