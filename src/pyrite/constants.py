from __future__ import annotations

from typing import TYPE_CHECKING

import cffi

if TYPE_CHECKING:
    pass

COMPONENT_TYPE: int = 2 ** (cffi.FFI().sizeof("int") * 8 - 1) - 1
