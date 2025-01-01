import pathlib
import sys
import unittest


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite._data_classes.entity_manager import (  # noqa:E402
    EntityManager,
    Entity,
    Renderable,
    UIElement,
)


class TestEntity(Entity):

    pass


class TestRenderable(Renderable):

    def render(self, delta_time: float):
        return super().render(delta_time)


class TestUIElement(UIElement):

    def render_ui(self, delta_time: float):
        return super().render_ui(delta_time)


class TestRenderableEntity(Renderable, Entity):

    def render(self, delta_time: float):
        return super().render(delta_time)


class TestUIEntity(UIElement, Entity):

    def render_ui(self, delta_time: float):
        return super().render_ui(delta_time)


class Test_Metadata(unittest.TestCase):

    def setUp(self) -> None:
        self.entity_manager = EntityManager()

    def test_enable(self):
        bare_entities = [TestEntity() for i in range(5)]
        bare_renderables = [TestRenderable() for i in range(5)]
        bare_ui_elements = [TestUIElement() for i in range(5)]
        renderable_entities = [TestRenderableEntity() for i in range(5)]
        ui_entities = [TestUIEntity() for i in range(5)]

        for item in [
            *bare_entities,
            *bare_renderables,
            *bare_ui_elements,
            *renderable_entities,
            *ui_entities,
        ]:
            self.entity_manager.enable(item)

        for entity in [*bare_entities, *renderable_entities, *ui_entities]:
            self.assertIn(entity, self.entity_manager.entities)

        for renderable in [*bare_renderables, *renderable_entities]:
            self.assertIn(renderable, self.entity_manager.renderables)

        for element in [*bare_ui_elements, *ui_entities]:
            self.assertIn(element, self.entity_manager.ui_elements)

    def test_disable(self):
        bare_entities = [TestEntity() for i in range(5)]
        bare_renderables = [TestRenderable() for i in range(5)]
        bare_ui_elements = [TestUIElement() for i in range(5)]
        renderable_entities = [TestRenderableEntity() for i in range(5)]
        ui_entities = [TestUIEntity() for i in range(5)]

        for item in [
            *bare_entities,
            *bare_renderables,
            *bare_ui_elements,
            *renderable_entities,
            *ui_entities,
        ]:
            self.entity_manager.enable(item)

        # Disable select member types
        for item in [
            *bare_entities,
            *bare_ui_elements,
            *renderable_entities,
        ]:
            self.entity_manager.disable(item)

        for entity in [*ui_entities]:
            self.assertIn(entity, self.entity_manager.entities)

        for entity in [*bare_entities, *renderable_entities]:
            self.assertNotIn(entity, self.entity_manager.entities)

        for renderable in [*bare_renderables]:
            self.assertIn(renderable, self.entity_manager.renderables)

        for renderable in [*renderable_entities]:
            self.assertNotIn(renderable, self.entity_manager.renderables)

        for element in [*ui_entities]:
            self.assertIn(element, self.entity_manager.ui_elements)

        for element in [*bare_ui_elements]:
            self.assertNotIn(element, self.entity_manager.ui_elements)


if __name__ == "__main__":

    unittest.main()
