import re

area_regex = re.compile(r"(\d{2})-(\d{2})")
category_regex = re.compile(r"(\d{2})")
id_regex = re.compile(r"(\d{2}).(\d{2})")


def _parse_area_number(string):
    # BBB: walrus operator
    m = area_regex.fullmatch(string)
    if m:
        a, b = map(int, m.groups())
        if a in range(10, 91, 10) and b == a + 9:
            return "area", (a, b)


def _parse_category_number(string):
    # BBB: walrus operator
    m = category_regex.fullmatch(string)
    if m:
        a = int(m.group(0))
        if 10 <= a <= 99 and a % 10 != 0:
            return "category", a


def _parse_id_number(string):
    # BBB: walrus operator
    m = id_regex.fullmatch(string)
    if m:
        a, b = map(int, m.groups())
        if 11 <= a <= 99 and a % 10 != 0 and 1 <= b <= 99:
            return "id", (a, b)


def parse_number(string):
    # XXX: return `(None, None)` or simply `None` as default?
    return (
        _parse_area_number(string)
        or _parse_category_number(string)
        or _parse_id_number(string)
        or (None, None)
    )


def valid_area_numbers():
    for x in range(10, 91, 10):
        yield x, x + 9


def valid_category_numbers(parent_info):
    lower, upper = parent_info.number_data
    return range(lower, upper + 1)


def valid_id_numbers(parent_info):
    for x in range(1, 100):
        yield parent_info.number_data, x


def format_number(type, data):
    if type == "area":
        return "%02d-%02d" % data
    elif type == "category":
        return str(data)
    elif type == "id":
        return "%02d.%02d" % data
    else:
        raise NotImplementedError(f"{type} is not supported")
