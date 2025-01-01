import pathlib
import sys
import unittest


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite._data_classes.metadata import Metadata  # noqa:E402


class Test_Metadata(unittest.TestCase):

    def test_get_metadata(self):
        test_name = "Test"
        test_caption = "Test caption"
        test_icon = None
        # Default case (Metadata object supplied)
        test_data = Metadata(
            name=test_name,
            caption=test_caption,
            icon=test_icon,
        )

        kwds = {"metadata": test_data}

        self.assertIs(test_data, Metadata.get_metadata(**kwds))

        # ideal case (All settings, no extras)
        kwds = {
            "name": test_name,
            "caption": test_caption,
            "icon": test_icon,
        }

        test_data = Metadata.get_metadata(**kwds)

        self.assertEqual(test_data.name, test_name)
        self.assertEqual(test_data.caption, test_caption)
        self.assertIs(test_data.icon, test_icon)

        # All settings, extras
        kwds = {
            "name": test_name,
            "caption": test_caption,
            "icon": test_icon,
            "foo": "bar",
        }

        test_data = Metadata.get_metadata(**kwds)

        self.assertEqual(test_data.name, test_name)
        self.assertEqual(test_data.caption, test_caption)
        self.assertIs(test_data.icon, test_icon)

        # missing settings, no extras
        kwds = {
            "name": test_name,
            "icon": test_icon,
        }

        test_data = Metadata.get_metadata(**kwds)

        self.assertEqual(test_data.name, test_name)
        self.assertEqual(test_data.caption, test_name)
        self.assertIs(test_data.icon, test_icon)

        # missing settings, extras
        kwds = {
            "name": test_name,
            "icon": test_icon,
            "foo": "bar",
        }

        test_data = Metadata.get_metadata(**kwds)

        self.assertEqual(test_data.name, test_name)
        self.assertEqual(test_data.caption, test_name)
        self.assertIs(test_data.icon, test_icon)

        # no settings, no extras
        kwds = {}

        test_data = Metadata.get_metadata(**kwds)

        self.assertEqual(test_data.name, "Game")
        self.assertEqual(test_data.caption, "Game")
        self.assertIs(test_data.icon, test_icon)

        # no settings, extras
        kwds = {"foo": "bar"}

        test_data = Metadata.get_metadata(**kwds)

        self.assertEqual(test_data.name, "Game")
        self.assertEqual(test_data.caption, "Game")
        self.assertIs(test_data.icon, test_icon)


if __name__ == "__main__":

    unittest.main()
