from __future__ import annotations

from typing import Any, TYPE_CHECKING
from weakref import WeakValueDictionary

from ..transform import TransformComponent
from ..types import Component
from .physics_service import PhysicsService

if TYPE_CHECKING:
    from pymunk import Body


class RigidbodyComponent(Component):
    _bodies: WeakValueDictionary[Body, Any] = WeakValueDictionary()
    """
    Associates an owner object with a physics body
    """

    def __init__(self, owner: Any, body: Body) -> None:
        super().__init__(owner)
        if not (transform := TransformComponent.get(owner)):
            raise RuntimeError(
                f"RigidbodyComponent requires that {owner} has a TransformComponent"
            )
        self.transform = transform
        self.body = body
        self._bodies.update({body: owner})
        PhysicsService.space.add(body)

    @classmethod
    def get_owner_from_body(cls, body: Body) -> Any | None:
        return cls._bodies.get(body)
