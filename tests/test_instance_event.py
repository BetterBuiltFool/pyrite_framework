import pathlib
import sys
import unittest


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.types.instance_event import InstanceEvent  # noqa:E402


class OnTestEvent(InstanceEvent):

    def __call__(self, *args: pathlib.Any, **kwds: pathlib.Any) -> None:
        return super().__call__(*args, **kwds)


class TestInstanceEvent(unittest.TestCase):

    pass


if __name__ == "__main__":

    unittest.main()
