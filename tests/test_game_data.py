import unittest

from pyrite.core.game_info import GameInfo


class Test_GameInfo(unittest.TestCase):

    def test_get_game_info(self):
        test_title = "Test"
        test_caption = "Test caption"
        test_icon = None
        # Default case (Metadata object supplied)
        test_data = GameInfo(
            title=test_title,
            caption=test_caption,
            icon=test_icon,
        )

        kwds = {"game_info": test_data}

        self.assertIs(test_data, GameInfo.get_game_info(**kwds))

        # ideal case (All settings, no extras)
        kwds = {
            "title": test_title,
            "caption": test_caption,
            "icon": test_icon,
        }

        test_data = GameInfo.get_game_info(**kwds)

        self.assertEqual(test_data.title, test_title)
        self.assertEqual(test_data.caption, test_caption)
        self.assertIs(test_data.icon, test_icon)

        # All settings, extras
        kwds = {
            "title": test_title,
            "caption": test_caption,
            "icon": test_icon,
            "foo": "bar",
        }

        test_data = GameInfo.get_game_info(**kwds)

        self.assertEqual(test_data.title, test_title)
        self.assertEqual(test_data.caption, test_caption)
        self.assertIs(test_data.icon, test_icon)

        # missing settings, no extras
        kwds = {
            "title": test_title,
            "icon": test_icon,
        }

        test_data = GameInfo.get_game_info(**kwds)

        self.assertEqual(test_data.title, test_title)
        self.assertEqual(test_data.caption, None)
        self.assertIs(test_data.icon, test_icon)

        # missing settings, extras
        kwds = {
            "title": test_title,
            "icon": test_icon,
            "foo": "bar",
        }

        test_data = GameInfo.get_game_info(**kwds)

        self.assertEqual(test_data.title, test_title)
        self.assertEqual(test_data.caption, None)
        self.assertIs(test_data.icon, test_icon)

        # no settings, no extras
        kwds = {}

        test_data = GameInfo.get_game_info(**kwds)

        self.assertEqual(test_data.title, "Game")
        self.assertEqual(test_data.caption, None)
        self.assertIs(test_data.icon, test_icon)

        # no settings, extras
        kwds = {"foo": "bar"}

        test_data = GameInfo.get_game_info(**kwds)

        self.assertEqual(test_data.title, "Game")
        self.assertEqual(test_data.caption, None)
        self.assertIs(test_data.icon, test_icon)


if __name__ == "__main__":

    unittest.main()
