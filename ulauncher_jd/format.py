import re

area_regex = re.compile(r"(\d{2})-(\d{2})")
category_regex = re.compile(r"(\d{2})")


def _match_area_type(string):
    # BBB: walrus operator
    m = area_regex.fullmatch(string)
    if not m:
        return False
    a, b = map(int, m.groups())
    if a not in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
        return False
    return b == (a + 9)


def _match_category_type(string):
    # BBB: walrus operator
    m = category_regex.fullmatch(string)
    if not m:
        return False
    a = int(m.group(0))
    return 10 <= a <= 99 and a % 10 != 0


def match_type(string):
    if _match_area_type(string):
        return "area"
    if _match_category_type(string):
        return "category"
