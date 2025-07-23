from __future__ import annotations
import unittest

from pyrite.transform import TransformComponent
from pyrite.services import TransformService
from pyrite.services.transform_service.transform_service import DefaultTransformService


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


if __name__ == "__main__":
    unittest.main()
