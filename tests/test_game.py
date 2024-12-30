import pathlib
import sys
import unittest


sys.path.append(str(pathlib.Path.cwd()))

from src.pyrite.game import Game  # noqa:E402


class Test(Game):

    def __init__(self, **kwds) -> None:
        super().__init__(**kwds)
        # Using this to test if a function was called
        self.activated = False


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.game = Test(suppress_init=True)

    def test_monkeypatch_method(self):

        def update(self: Test, delta_time: float) -> None:
            self.activated = True

        self.game.update(0)
        self.assertFalse(self.game.activated)

        self.game._monkeypatch_method(self.game.update, update)

        self.game.update(0)
        self.assertTrue(self.game.activated)


if __name__ == "__main__":

    unittest.main()
