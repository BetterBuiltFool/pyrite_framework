from __future__ import annotations

from abc import ABC  # , abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .rigidbody_component import RigidbodyComponent


class Constraint(ABC):
    """
    ABC class for physics contraints. All constraints are adapters for the underlying
    physics engine.
    """

    def __init__(self, body_a: RigidbodyComponent, body_b: RigidbodyComponent) -> None:
        self._a = body_a
        self._b = body_b

    @property
    def a(self) -> RigidbodyComponent:
        """
        The first of the two constrained rigidbodies.
        """
        return self._a

    @property
    def b(self) -> RigidbodyComponent:
        """
        The second of the two constrained rigidbodies.
        """
        return self._b
