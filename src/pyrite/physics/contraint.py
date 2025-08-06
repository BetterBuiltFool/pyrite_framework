from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .rigidbody_component import RigidbodyComponent


class Constraint(ABC):

    @property
    @abstractmethod
    def a(self) -> RigidbodyComponent:
        """
        The first of the two constrained rigidbodies.
        """
        pass

    @a.setter
    @abstractmethod
    def a(self, body: RigidbodyComponent) -> None:
        pass

    @property
    @abstractmethod
    def b(self) -> RigidbodyComponent:
        """
        The second of the two constrained rigidbodies.
        """
        pass

    @b.setter
    @abstractmethod
    def b(self, body: RigidbodyComponent) -> None:
        pass
