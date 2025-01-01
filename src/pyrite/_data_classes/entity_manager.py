from weakref import WeakSet

from src.pyrite.types.entity import Entity
from src.pyrite.types.renderable import Renderable


class EntityManager:

    def __init__(self) -> None:
        self.updateables: WeakSet[Entity] = WeakSet()
        self.renderables: WeakSet[Renderable] = WeakSet()

    def enable(self, item: Entity | Renderable) -> None:
        if isinstance(item, Entity):
            self.updateables.add(item)
        if isinstance(item, Renderable):
            self.renderables.add(item)

    def disable(self, item: Entity | Renderable) -> None:
        self.updateables.discard(item)
        self.renderables.discard(item)
