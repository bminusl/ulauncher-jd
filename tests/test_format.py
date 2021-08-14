# flake8: noqa
# fmt: off

import unittest

from ulauncher_jd import ComponentInfo
from ulauncher_jd.format import (
    format_number,
    parse_number,
    valid_area_numbers,
    valid_category_numbers,
    valid_id_numbers,
)


class FormatTest(unittest.TestCase):
    def test_parse_number(self):
        self.assertEqual(parse_number("30-39"), ("area", (30, 39)))

        self.assertEqual(parse_number("42"), ("category", 42))

        self.assertEqual(parse_number("53.45"), ("id", (53, 45)))
        self.assertEqual(parse_number("53.09"), ("id", (53, 9)))

        self.assertEqual(parse_number("whatever"), (None, None))

        self.assertEqual(parse_number("100-10"), (None, None))
        self.assertEqual(parse_number("100-100"), (None, None))
        self.assertEqual(parse_number("10-100"), (None, None))
        self.assertEqual(parse_number("aa-bb"), (None, None))

        self.assertEqual(parse_number("100"), (None, None))
        self.assertEqual(parse_number("-100"), (None, None))
        self.assertEqual(parse_number("a"), (None, None))

        self.assertEqual(parse_number("100.10"), (None, None))
        self.assertEqual(parse_number("100.100"), (None, None))
        self.assertEqual(parse_number("10.100"), (None, None))
        self.assertEqual(parse_number("aa.bb"), (None, None))

    def test_valid_area_numbers(self):
        self.assertEqual(list(valid_area_numbers()),
                         [(10, 19), (20, 29), (30, 39), (40, 49), (50, 59), (60, 69), (70, 79), (80, 89), (90, 99)])

    def test_valid_category_numbers(self):
        parent_info = ComponentInfo(type='area', abspath='/jd/30-39 Marketing', number='30-39', number_data=(30, 39))
        self.assertEqual(list(valid_category_numbers(parent_info)), [31, 32, 33, 34, 35, 36, 37, 38, 39])

    def test_valid_id_numbers(self):
        parent_info = ComponentInfo(type='category', abspath='/jd/10-19 Finance/12 Payroll', number='12', number_data=12)
        self.assertEqual(list(valid_id_numbers(parent_info)),
                         [(12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13), (12, 14), (12, 15), (12, 16), (12, 17), (12, 18), (12, 19), (12, 20), (12, 21), (12, 22), (12, 23), (12, 24), (12, 25), (12, 26), (12, 27), (12, 28), (12, 29), (12, 30), (12, 31), (12, 32), (12, 33), (12, 34), (12, 35), (12, 36), (12, 37), (12, 38), (12, 39), (12, 40), (12, 41), (12, 42), (12, 43), (12, 44), (12, 45), (12, 46), (12, 47), (12, 48), (12, 49), (12, 50), (12, 51), (12, 52), (12, 53), (12, 54), (12, 55), (12, 56), (12, 57), (12, 58), (12, 59), (12, 60), (12, 61), (12, 62), (12, 63), (12, 64), (12, 65), (12, 66), (12, 67), (12, 68), (12, 69), (12, 70), (12, 71), (12, 72), (12, 73), (12, 74), (12, 75), (12, 76), (12, 77), (12, 78), (12, 79), (12, 80), (12, 81), (12, 82), (12, 83), (12, 84), (12, 85), (12, 86), (12, 87), (12, 88), (12, 89), (12, 90), (12, 91), (12, 92), (12, 93), (12, 94), (12, 95), (12, 96), (12, 97), (12, 98), (12, 99)])

    def test_format_number(self):
        self.assertEqual(format_number("area", (30, 39)), "30-39")

        self.assertEqual(format_number("category", 12), "12")

        self.assertEqual(format_number("id", (12, 1)), "12.01")
        self.assertEqual(format_number("id", (34,52)), "34.52")

        self.assertRaises(NotImplementedError, format_number, "whatever", None)


if __name__ == "__main__":
    unittest.main()
