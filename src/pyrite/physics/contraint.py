from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .rigidbody_component import RigidbodyComponent


class Constraint(ABC):
    """
    ABC class for physics contraints. All constraints are adapters for the underlying
    physics engine.
    """

    @property
    @abstractmethod
    def a(self) -> RigidbodyComponent:
        """
        The first of the two constrained rigidbodies.
        """
        pass

    @property
    @abstractmethod
    def b(self) -> RigidbodyComponent:
        """
        The second of the two constrained rigidbodies.
        """
        pass
