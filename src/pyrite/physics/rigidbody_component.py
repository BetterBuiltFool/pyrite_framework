from __future__ import annotations

from collections.abc import KeysView
from typing import Any, TYPE_CHECKING
from weakref import ref, WeakKeyDictionary

from pygame import Vector2
from pymunk import Body

from ..transform import TransformComponent
from ..component import Component
from ..services import PhysicsService

if TYPE_CHECKING:
    from .collider_component import ColliderComponent
    from ..types.constraint import Constraint


class RigidbodyComponent(Component):
    """
    Associates an owner object with a physics body.

    Requires a TransformComponent.

    Required for ColliderComponent and KinematicComponent.
    """

    def __init__(self, owner: Any, body: Body | None = None) -> None:
        super().__init__(owner)
        if not (transform := TransformComponent.get(owner)):
            raise RuntimeError(
                f"RigidbodyComponent requires that {owner} has a TransformComponent"
            )
        if body is None:
            body = Body()
        self.transform = transform
        self.body = body
        self.body.position = tuple(transform.world_position)
        self.body.angle = transform.world_rotation

        self._constraints: WeakKeyDictionary[Constraint, None] = WeakKeyDictionary()

        self._collider: ref[ColliderComponent] | None = None  # TODO: Remove this
        PhysicsService.add_rigidbody(self)

    @property
    def center_of_gravity(self) -> Vector2:
        """
        Returns the local center of gravity for the rigidbody.
        """
        return Vector2(self.body.center_of_gravity)

    @property
    def constraints(self) -> KeysView[Constraint]:
        """
        Provides the constraints the rigidbody is attached to.
        """
        return KeysView(self._constraints)

    @property
    def mass(self) -> float:
        """
        The mass value of the rigidbody.
        """
        return self.body.mass

    @mass.setter
    def mass(self, mass: float) -> None:
        self.body.mass = mass

    @property
    def moment(self) -> float:
        """
        Moment of Inertia for the rigidbody. Represents resistance to change in
        rotation.

        Rotation can be disabled with `rigidbody.moment = float('inf')`
        """
        return self.body.moment

    @moment.setter
    def moment(self, moment: float) -> None:
        self.body.moment = moment

    @property
    def position(self) -> Vector2:
        """
        Returns A Vector2 of the world position of the Rigidbody, as reported by the
        underlying physics engine.

        Does not respect the values of any associated TransformComponents.
        """
        return Vector2(self.body.position)

    @property
    def is_sleeping(self) -> bool:
        """
        Returns True if the rigidbody is sleeping.
        """
        return self.body.is_sleeping

    def sleep(self) -> None:
        """
        Forces the rigidbody to sleep, regardless of circumstances.
        """
        self.body.sleep()

    def sleep_with_group(self, component: RigidbodyComponent) -> None:
        """
        Forces the rigidbody to sleep, while putting it into the same group as the
        passed component.

        :param component: Another rigidbody component, with whom the calling component
        will be grouped.
        """
        self.body.sleep_with_group(component.body)
