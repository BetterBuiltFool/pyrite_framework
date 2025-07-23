from __future__ import annotations
import unittest

# from pyrite.transform import Transform, TransformComponent
from pyrite.services.transform_service.transform_service import DefaultTransformService


class Empty:

    pass


class TestDefaultTransformService(unittest.TestCase):

    def setUp(self) -> None:
        self.transform_service = DefaultTransformService()


if __name__ == "__main__":
    unittest.main()
