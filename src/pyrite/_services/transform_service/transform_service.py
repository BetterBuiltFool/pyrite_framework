from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from weakref import WeakKeyDictionary, WeakSet

from pygame import Vector2
from weaktree import WeakTreeNode

from pyrite._types.service import Service

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pygame.typing import Point
    from pyrite._transform.transform import Transform
    from pyrite._component.transform_component import TransformComponent

    type NodeDict = WeakKeyDictionary[
        TransformComponent, WeakTreeNode[TransformComponent]
    ]


class TransformService(Service):

    @abstractmethod
    def __iter__(self) -> Iterator[TransformComponent | None]:
        pass

    @abstractmethod
    def frame_reset(self) -> None:
        pass

    @abstractmethod
    def get_local(self, component: TransformComponent) -> Transform:
        pass

    @abstractmethod
    def get_local_position(self, component: TransformComponent) -> Vector2:
        pass

    @abstractmethod
    def get_local_rotation(self, component: TransformComponent) -> float:
        pass

    @abstractmethod
    def get_local_scale(self, component: TransformComponent) -> Vector2:
        pass

    @abstractmethod
    def set_local(self, component: TransformComponent, value: Transform):
        pass

    @abstractmethod
    def set_local_position(self, component: TransformComponent, position: Point):
        pass

    @abstractmethod
    def set_local_rotation(self, component: TransformComponent, angle: float):
        pass

    @abstractmethod
    def set_local_scale(self, component: TransformComponent, scale: Point):
        pass

    @abstractmethod
    def get_world(self, component: TransformComponent) -> Transform:
        pass

    @abstractmethod
    def get_world_position(self, component: TransformComponent) -> Vector2:
        pass

    @abstractmethod
    def get_world_rotation(self, component: TransformComponent) -> float:
        pass

    @abstractmethod
    def get_world_scale(self, component: TransformComponent) -> Vector2:
        pass

    @abstractmethod
    def set_world(self, component: TransformComponent, value: Transform):
        pass

    @abstractmethod
    def _set_world_no_update(self, component: TransformComponent, value: Transform):
        pass

    @abstractmethod
    def set_world_position(self, component: TransformComponent, position: Point):
        pass

    @abstractmethod
    def set_world_rotation(self, component: TransformComponent, angle: float):
        pass

    @abstractmethod
    def set_world_scale(self, component: TransformComponent, scale: Point):
        pass

    @abstractmethod
    def get_relative_of(
        self, component: TransformComponent
    ) -> TransformComponent | None:
        pass

    @abstractmethod
    def set_relative_to(
        self, dependent: TransformComponent, relative: TransformComponent
    ) -> None:
        pass

    @abstractmethod
    def get_dependents(self, component: TransformComponent) -> set[TransformComponent]:
        pass

    @abstractmethod
    def make_dirty(self, component: TransformComponent) -> None:
        pass

    @abstractmethod
    def is_dirty(self, component: TransformComponent) -> bool:
        pass

    @abstractmethod
    def clean(self, component: TransformComponent):
        pass

    @abstractmethod
    def get_dirty(
        self,
    ) -> set[TransformComponent]:
        pass

    @abstractmethod
    def mark_changed(self, transform: TransformComponent) -> None:
        pass

    @abstractmethod
    def has_changed(self, component: TransformComponent) -> bool:
        pass

    @abstractmethod
    def get_changed(self) -> set[TransformComponent]:
        pass

    @abstractmethod
    def initialize_component(self, component: TransformComponent, value: Transform):
        pass


class DefaultTransformService(TransformService):
    def __init__(self) -> None:
        self.world_transforms: WeakKeyDictionary[TransformComponent, Transform] = (
            WeakKeyDictionary()
        )
        self.local_transforms: WeakKeyDictionary[TransformComponent, Transform] = (
            WeakKeyDictionary()
        )
        self.root_transforms: WeakSet[WeakTreeNode[TransformComponent]] = WeakSet()
        self.transform_nodes: NodeDict = WeakKeyDictionary()

        self.dirty_components: WeakSet[TransformComponent] = WeakSet()

        self.changed_components: WeakSet[TransformComponent] = WeakSet()

    def __iter__(self) -> Iterator[TransformComponent | None]:
        for node in self.root_transforms:
            yield from node.values().depth()

    def frame_reset(self) -> None:
        self.changed_components = WeakSet()

    def transfer(self, target_service: TransformService):
        for component, transform in self.local_transforms.items():
            target_service.initialize_component(component, transform)

    def get_local(self, component: TransformComponent) -> Transform:
        return self.local_transforms[component]

    def get_local_position(self, component: TransformComponent) -> Vector2:
        return self.local_transforms[component].position

    def get_local_rotation(self, component: TransformComponent) -> float:
        return self.local_transforms[component].rotation

    def get_local_scale(self, component: TransformComponent) -> Vector2:
        return self.local_transforms[component].scale

    def set_local(self, component: TransformComponent, value: Transform):
        self.local_transforms[component] = value

    def set_local_position(self, component: TransformComponent, position: Point):
        self.dirty_components.add(component)
        self.local_transforms[component].position = Vector2(position)

    def set_local_rotation(self, component: TransformComponent, angle: float):
        self.dirty_components.add(component)
        self.local_transforms[component].rotation = angle

    def set_local_scale(self, component: TransformComponent, scale: Point):
        self.dirty_components.add(component)
        self.local_transforms[component].scale = Vector2(scale)

    def get_world(self, component: TransformComponent) -> Transform:
        return self.world_transforms[component]

    def get_world_position(self, component: TransformComponent) -> Vector2:
        return self.world_transforms[component].position

    def get_world_rotation(self, component: TransformComponent) -> float:
        return self.world_transforms[component].rotation

    def get_world_scale(self, component: TransformComponent) -> Vector2:
        return self.world_transforms[component].scale

    def set_world(self, component: TransformComponent, value: Transform):
        self._set_world_no_update(component, value)
        self.changed_components.add(component)

        local_transform = self._calc_local_from_world(component, value)
        self.local_transforms[component] = local_transform

    def _set_world_no_update(self, component: TransformComponent, value: Transform):
        self.world_transforms[component] = value

    def set_world_position(self, component: TransformComponent, position: Point):
        self.world_transforms[component].position = Vector2(position)

    def set_world_rotation(self, component: TransformComponent, angle: float):
        self.world_transforms[component].rotation = angle

    def set_world_scale(self, component: TransformComponent, scale: Point):
        self.world_transforms[component].scale = Vector2(scale)

    def _calc_local_from_world(
        self, component: TransformComponent, value: Transform
    ) -> Transform:
        node = self.transform_nodes[component]
        if not (trunk := node.trunk) or not (trunk_transform := trunk.data):
            return value.copy()
        return value.new(value / trunk_transform.world())

    def _calc_world_from_local(
        self, component: TransformComponent, value: Transform
    ) -> Transform:
        node = self.transform_nodes[component]
        if not (trunk := node.trunk) or not (trunk_transform := trunk.data):
            return value.copy()
        return value.new(trunk_transform.world() * value)

    def get_relative_of(
        self, component: TransformComponent
    ) -> TransformComponent | None:
        node = self.transform_nodes[component]
        if not (node_trunk := node.trunk):
            return None
        return node_trunk.data

    def set_relative_to(
        self, dependent: TransformComponent, relative: TransformComponent | None
    ) -> None:
        component_node = self.transform_nodes[dependent]

        if not relative:
            component_node.trunk = None
            self.root_transforms.add(component_node)
            return

        parent_node = self.transform_nodes[relative]

        if not self._validate_parent(component_node, parent_node):
            raise ValueError(
                f"Cannot set {relative} as parent to {dependent}; {dependent} is an"
                f" ancestor to {relative}"
            )
        component_node.trunk = parent_node
        self.root_transforms.discard(component_node)

    def _validate_parent(
        self,
        node: WeakTreeNode[TransformComponent],
        parent: WeakTreeNode[TransformComponent],
    ) -> bool:
        for trunk_node in parent.towards_root():
            if trunk_node is node:
                return False
        return True

    def get_dependents(self, component: TransformComponent) -> set[TransformComponent]:
        node = self.transform_nodes[component]
        descendants: set[TransformComponent] = set()
        for branch in node.branches:
            if not (descendant := branch.data):
                continue
            descendants.add(descendant)
        return descendants

    def make_dirty(self, component: TransformComponent) -> None:
        self.dirty_components.add(component)

    def is_dirty(self, component: TransformComponent) -> bool:
        return component in self.dirty_components

    def clean(self, component: TransformComponent):
        world_transform = self._calc_world_from_local(component, component.raw())
        self._set_world_no_update(component, world_transform)
        self.dirty_components.discard(component)
        self.changed_components.add(component)

    def get_dirty(self) -> set[TransformComponent]:
        return set(self.dirty_components)

    def mark_changed(self, transform: TransformComponent) -> None:
        self.changed_components.add(transform)

    def has_changed(self, component: TransformComponent) -> bool:
        return component in self.changed_components

    def get_changed(self) -> set[TransformComponent]:
        return set(self.changed_components)

    def initialize_component(self, component: TransformComponent, value: Transform):
        self.dirty_components.add(component)
        self.local_transforms[component] = value
        # Temporary, will update w/ TransformComponent updates
        self.world_transforms[component] = value.copy()

        node = WeakTreeNode(component, cleanup_mode=WeakTreeNode.REPARENT)
        self.transform_nodes[component] = node
        self.root_transforms.add(node)
