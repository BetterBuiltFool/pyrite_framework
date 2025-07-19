from __future__ import annotations

from abc import abstractmethod
from typing import TypeAlias, TYPE_CHECKING

from weakref import WeakKeyDictionary, WeakSet

from pygame import Vector2
from weaktree import WeakTreeNode

from ...types.service import Service

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pygame.typing import Point
    from ...transform import Transform, TransformComponent

    NodeDict: TypeAlias = WeakKeyDictionary[
        TransformComponent, WeakTreeNode[TransformComponent]
    ]


class TransformService(Service):

    @abstractmethod
    def __iter__(self) -> Iterator[TransformComponent | None]:
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
    def set_world_position(self, component: TransformComponent, position: Point):
        pass

    @abstractmethod
    def set_world_rotation(self, component: TransformComponent, angle: float):
        pass

    @abstractmethod
    def set_world_scale(self, component: TransformComponent, scale: Point):
        pass

    @abstractmethod
    def get_parent(self, component: TransformComponent) -> TransformComponent | None:
        pass

    @abstractmethod
    def set_parent(
        self, component: TransformComponent, parent: TransformComponent
    ) -> None:
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
        self.root_transforms: list[WeakTreeNode[TransformComponent]] = []
        self.transform_nodes: NodeDict = WeakKeyDictionary()

        self.dirty_components: WeakSet[TransformComponent] = WeakSet()

    def __iter__(self) -> Iterator[TransformComponent | None]:
        for node in self.root_transforms:
            yield from node.values().depth()

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
        self.local_transforms.update({component: value})

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
        # TODO Force update local
        self.world_transforms.update({component: value})

    def set_world_position(self, component: TransformComponent, position: Point):
        # TODO Force update local
        self.world_transforms[component].position = Vector2(position)

    def set_world_rotation(self, component: TransformComponent, angle: float):
        # TODO Force update local
        self.world_transforms[component].rotation = angle

    def set_world_scale(self, component: TransformComponent, scale: Point):
        # TODO Force update local
        self.world_transforms[component].scale = Vector2(scale)

    def get_parent(self, component: TransformComponent) -> TransformComponent | None:
        node = self.transform_nodes[component]
        if not (node_trunk := node.trunk):
            return None
        return node_trunk.data

    def set_parent(
        self, component: TransformComponent, parent: TransformComponent
    ) -> None:
        component_node = self.transform_nodes[component]
        parent_node = self.transform_nodes[parent]

        # TODO: This permits parent loops, which is undesireable. Add a validation
        # method.
        component_node.trunk = parent_node
        self.root_transforms.remove(component_node)

    def is_dirty(self, component: TransformComponent) -> bool:
        return component in self.dirty_components

    def clean(self, component: TransformComponent):
        self.dirty_components.discard(component)

    def get_dirty(self) -> set[TransformComponent]:
        return set(self.dirty_components)

    def initialize_component(self, component: TransformComponent, value: Transform):
        self.dirty_components.add(component)
        self.local_transforms.update({component: value})
        # Temporary, will update w/ TransformComponent updates
        self.world_transforms.update({component: value.copy()})

        node = WeakTreeNode(component, cleanup_mode=WeakTreeNode.REPARENT)
        self.transform_nodes[component] = node
        self.root_transforms.append(node)
