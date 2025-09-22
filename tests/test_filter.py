from __future__ import annotations

import unittest

from pyrite._physics.filter import Filter
from pyrite.constants import MASK_ALL


class TestFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.filters: dict[str, Filter] = {
            "a": Filter(0, 1, 2),
            "b": Filter(0, 4, 4),
            "c": Filter(0, 3, 1),
            "d": Filter(0, MASK_ALL, MASK_ALL),
        }
        self.a = Filter(0, 1, 2)
        self.b = Filter(0, 4, 4)
        self.c = Filter(0, 3, 1)
        self.d = Filter(0, MASK_ALL, MASK_ALL)

    def generate_rejects_dict(self) -> dict[str, tuple[Filter, Filter]]:
        cases: dict[str, tuple[Filter, Filter]] = {}
        keys = list(self.filters.keys())
        for index, key in enumerate(keys):
            for i in range(index, len(keys)):
                if key == keys[i]:
                    continue
                case_label = f"{key}-{keys[i]}"
                params = (self.filters[key], self.filters[keys[i]])
                cases[case_label] = params
        return cases

    def test_rejects_collision(self) -> None:
        expected: dict[str, bool] = {
            "a-b": True,
            "a-c": False,
            "a-d": False,
            "b-c": True,
            "b-d": False,
            "c-d": False,
        }
        cases = self.generate_rejects_dict()
        for index, (case, params) in enumerate(cases.items()):
            with self.subTest(case, i=index):
                self.assertEqual(params[0].rejects_collision(params[1]), expected[case])


if __name__ == "__main__":

    unittest.main()
