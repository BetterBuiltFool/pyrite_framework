from weakref import WeakSet

from src.pyrite.types.entity import Entity
from src.pyrite.types.renderable import Renderable, UIElement


class EntityManager:

    def __init__(self) -> None:
        self.entities: WeakSet[Entity] = WeakSet()
        self.renderables: WeakSet[Renderable] = WeakSet()
        self.ui_elements: WeakSet[UIElement] = WeakSet()

    def enable(self, item: Entity | Renderable) -> None:
        if isinstance(item, Entity):
            self.entities.add(item)
        if isinstance(item, Renderable):
            self.renderables.add(item)
        if isinstance(item, UIElement):
            self.ui_elements.add(item)

    def disable(self, item: Entity | Renderable) -> None:
        self.entities.discard(item)
        self.renderables.discard(item)
        self.ui_elements.discard(item)
