# flake8: noqa
# fmt: off

import unittest
from unittest import mock

from ulauncher_jd import ComponentInfo, preferences
from ulauncher_jd.filesystem import find, next_available_component, search

# XXX: this is the same data, represented in two ways, TODO: refactor
walk_return_value = [
    ('/jd', ['10-19 Finance', '20-29 Administration', '30-39 Marketing', '40-49 Sales'], []),
    ('/jd/10-19 Finance', ["11 Tax returns", "12 Payroll", "13 Bookkeeping"], []),
    ('/jd/10-19 Finance/12 Payroll', ["12.01 Staff bank details for payments", "12.02 Payroll calculation spreadsheet", "12.03 Payroll schedule for 2018"], []),
    ('/jd/10-19 Finance/12 Payroll/12.01 Staff bank details for payments', [], []),
    ('/jd/10-19 Finance/12 Payroll/12.02 Payroll calculation spreadsheet', [], []),
    ('/jd/10-19 Finance/12 Payroll/12.03 Payroll schedule for 2018', [], []),
    ('/jd/20-29 Administration', ["21 Company registration"], []),
    ('/jd/20-29 Administration/21 Company registration', [], []),
    ('/jd/30-39 Marketing', [], []),
    ('/jd/40-49 Sales', [], []),
]
def listdir_side_effect(path):
    return {
        '/jd': ['10-19 Finance', '20-29 Administration', '30-39 Marketing', '40-49 Sales'],
        '/jd/10-19 Finance': ["11 Tax returns", "12 Payroll", "13 Bookkeeping"],
        '/jd/10-19 Finance/12 Payroll': ["12.01 Staff bank details for payments", "12.02 Payroll calculation spreadsheet", "12.03 Payroll schedule for 2018"],
        '/jd/10-19 Finance/12 Payroll/12.01 Staff bank details for payments': [],
        '/jd/10-19 Finance/12 Payroll/12.02 Payroll calculation spreadsheet': [],
        '/jd/10-19 Finance/12 Payroll/12.03 Payroll schedule for 2018': [],
        '/jd/20-29 Administration': ["21 Company registration"],
        '/jd/20-29 Administration/21 Company registration': [],
        '/jd/30-39 Marketing': [],
        '/jd/40-49 Sales': [],
    }[path]

#XXX: since os.walk uses os.listdir under the hood, we could stop patching it (but it needs work)
@mock.patch("os.walk", return_value=walk_return_value)
@mock.patch("os.listdir", side_effect=listdir_side_effect)
@mock.patch("os.path.isdir", return_value=True)
class FilesystemTest(unittest.TestCase):
    def test_search(self, mocked_walk, mocked_listdir, mocked_isdir):
        # numbers
        self.assertEqual(list(search("30-39")), [ComponentInfo(type='area', abspath='/jd/30-39 Marketing', number='30-39', number_data=(30, 39))])
        self.assertEqual(list(search("12")), [ComponentInfo(type='category', abspath='/jd/10-19 Finance/12 Payroll', number='12', number_data=12),
                                              ComponentInfo(type='id', abspath='/jd/10-19 Finance/12 Payroll/12.01 Staff bank details for payments', number='12.01', number_data=(12, 1)),
                                              ComponentInfo(type='id', abspath='/jd/10-19 Finance/12 Payroll/12.02 Payroll calculation spreadsheet', number='12.02', number_data=(12, 2)),
                                              ComponentInfo(type='id', abspath='/jd/10-19 Finance/12 Payroll/12.03 Payroll schedule for 2018', number='12.03', number_data=(12, 3))])
        self.assertEqual(list(search("12.02")), [ComponentInfo(type='id', abspath='/jd/10-19 Finance/12 Payroll/12.02 Payroll calculation spreadsheet', number='12.02', number_data=(12, 2))])
        self.assertEqual(list(search("42")), []) # Sorry, no answer to the big question

        # text, different cases
        self.assertEqual(list(search("admi")), [ComponentInfo(type='area', abspath='/jd/20-29 Administration', number='20-29', number_data=(20, 29))])
        self.assertEqual(list(search("Admi")), [ComponentInfo(type='area', abspath='/jd/20-29 Administration', number='20-29', number_data=(20, 29))])
        self.assertEqual(list(search("ADMI")), [ComponentInfo(type='area', abspath='/jd/20-29 Administration', number='20-29', number_data=(20, 29))])
        self.assertEqual(list(search("aDmI")), [ComponentInfo(type='area', abspath='/jd/20-29 Administration', number='20-29', number_data=(20, 29))])

        # text, multiple matches
        self.assertEqual(list(search("Payroll")), [ComponentInfo(type='category', abspath='/jd/10-19 Finance/12 Payroll', number='12', number_data=12),
                                                   ComponentInfo(type='id', abspath='/jd/10-19 Finance/12 Payroll/12.02 Payroll calculation spreadsheet', number='12.02', number_data=(12, 2)),
                                                   ComponentInfo(type='id', abspath='/jd/10-19 Finance/12 Payroll/12.03 Payroll schedule for 2018', number='12.03', number_data=(12, 3))])

    def test_find(self, mocked_walk, mocked_listdir, mocked_isdir):
        self.assertEqual(find("30-39"), ComponentInfo(type='area', abspath='/jd/30-39 Marketing', number='30-39', number_data=(30, 39)))
        self.assertEqual(find("12"), ComponentInfo(type='category', abspath='/jd/10-19 Finance/12 Payroll', number='12', number_data=12))
        self.assertEqual(find("12.02"), ComponentInfo(type='id', abspath='/jd/10-19 Finance/12 Payroll/12.02 Payroll calculation spreadsheet', number='12.02', number_data=(12, 2)))
        self.assertEqual(find("42"), None) # Sorry, no answer to the big question

    def test_next_available_component(self, mocked_walk, mocked_listdir, mocked_isdir):
        # new area (not empty root parent)
        self.assertEqual(next_available_component("foo bar baz",
                                                  preferences["basedir_info"]),
                         ComponentInfo(type='area', abspath='/jd/50-59 foo bar baz', number='50-59', number_data=(50, 59)))

        # new categories (empty parent area or not)
        self.assertEqual(next_available_component("spam ham eggs",
                                                  ComponentInfo(type='area', abspath='/jd/30-39 Marketing', number='30-39', number_data=(30, 39))),
                         ComponentInfo(type='category', abspath='/jd/30-39 Marketing/31 spam ham eggs', number='31', number_data=31))
        self.assertEqual(next_available_component("spam ham eggs",
                                                  ComponentInfo(type='area', abspath='/jd/10-19 Finance', number='10-19', number_data=(10, 19))),
                         ComponentInfo(type='category', abspath='/jd/10-19 Finance/14 spam ham eggs', number='14', number_data=14))

        # new ids (empty parent category or not)
        self.assertEqual(next_available_component("hello world",
                                                  ComponentInfo(type='category', abspath='/jd/20-29 Administration/21 Company registration', number='21', number_data=21)),
                         ComponentInfo(type='id', abspath='/jd/20-29 Administration/21 Company registration/21.01 hello world', number='21.01', number_data=(21, 1)))
        self.assertEqual(next_available_component("hello world",
                                                  ComponentInfo(type='category', abspath='/jd/10-19 Finance/12 Payroll', number='12', number_data=12)),
                         ComponentInfo(type='id', abspath='/jd/10-19 Finance/12 Payroll/12.04 hello world', number='12.04', number_data=(12, 4)))


if __name__ == "__main__":
    unittest.main()
