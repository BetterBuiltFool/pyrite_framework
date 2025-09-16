from __future__ import annotations
import unittest

from pyrite.transform import TransformComponent
from pyrite._services import TransformService
from pyrite._services.transform_service.transform_service import DefaultTransformService


class Empty:

    pass


class TestDefaultTransformService(unittest.TestCase):

    def setUp(self) -> None:
        self.transform_service = DefaultTransformService()

        # Ensure that when test objects are created, we know what service object they
        # are dealing with.
        TransformService.hotswap(self.transform_service)

    def test_initialize_component(self) -> None:
        root_component = TransformComponent(Empty())

        self.assertIn(root_component, self.transform_service.world_transforms)
        self.assertIn(root_component, self.transform_service.local_transforms)
        self.assertIn(root_component, self.transform_service.dirty_components)
        self.assertIn(root_component, self.transform_service.transform_nodes)

        root_node = self.transform_service.transform_nodes[root_component]

        self.assertIn(root_node, self.transform_service.root_transforms)

    def test_validate_parent(self):
        root_component = TransformComponent(Empty())
        branch_component = TransformComponent(Empty())

        self.transform_service.set_relative_to(branch_component, root_component)

        root_node = self.transform_service.transform_nodes[root_component]
        branch_node = self.transform_service.transform_nodes[branch_component]

        self.assertTrue(self.transform_service._validate_parent(branch_node, root_node))
        self.assertFalse(
            self.transform_service._validate_parent(root_node, branch_node)
        )

    def test_set_relative_to(self):
        root_component = TransformComponent(Empty())
        branch_component = TransformComponent(Empty())

        TransformService.set_relative_to(branch_component, root_component)

        self.assertIs(
            TransformService.get_relative_of(branch_component), root_component
        )

        with self.assertRaises(ValueError):
            self.transform_service.set_relative_to(root_component, branch_component)

    def test_make_dirty(self):
        root_component = TransformComponent(Empty())

        self.assertTrue(root_component.is_dirty())

        self.transform_service.dirty_components.clear()

        self.assertFalse(root_component.is_dirty())

        TransformService.make_dirty(root_component)

        self.assertTrue(root_component.is_dirty())

    def test_get_dependents(self):
        root_component = TransformComponent(Empty())
        branch_component = TransformComponent(Empty())

        TransformService.set_relative_to(branch_component, root_component)

        expected = set([branch_component])

        self.assertEqual(TransformService.get_dependents(root_component), expected)

    def test_get_relative_of(self):
        root_component = TransformComponent(Empty())
        branch_component = TransformComponent(Empty())

        TransformService.set_relative_to(branch_component, root_component)

        expected = root_component

        self.assertIs(TransformService.get_relative_of(branch_component), expected)


if __name__ == "__main__":
    unittest.main()
