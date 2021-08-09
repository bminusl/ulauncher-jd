import os

from . import BASEDIR, ComponentInfo
from .format import (
    format_number,
    parse_number,
    valid_area_numbers,
    valid_category_numbers,
    valid_id_numbers,
)


def search(query):
    query = query.lower()

    for root, dirs, files in os.walk(BASEDIR):

        depth = root.count(os.sep) - BASEDIR.count(os.sep)
        if depth > 2:
            continue

        for name in dirs:
            if query in name.lower():
                number = name.split()[0]
                type, number_data = parse_number(number)
                yield ComponentInfo(
                    type=type,
                    abspath=os.path.join(root, name),
                    number=number,
                    number_data=number_data,
                )


def find(number):
    # BBB: walrus operator
    desired_type = parse_number(number)[0]
    if not desired_type:
        return
    for result in search(number):
        if result.type == desired_type:
            return result


def next_available_component(new_name, parent_info):
    if parent_info.type is None:
        new_type = "area"
        valid_numbers = valid_area_numbers()
    elif parent_info.type == "area":
        new_type = "category"
        valid_numbers = valid_category_numbers(parent_info)
    elif parent_info.type == "category":
        new_type = "id"
        valid_numbers = valid_id_numbers(parent_info)
    else:
        raise Exception("This should never be triggered")

    present_numbers = []
    for name in sorted(os.listdir(parent_info.abspath)):
        if not os.path.isdir(os.path.join(parent_info.abspath, name)):
            continue

        number = name.split()[0]
        type, number_data = parse_number(number)
        if type == new_type:
            present_numbers.append(number_data)

    for candidate_data in valid_numbers:
        if candidate_data not in present_numbers:
            break
    else:
        # TODO: use custom exception class
        raise Exception("No valid number available")

    new_number = format_number(new_type, candidate_data)
    new_name = f"{new_number} {new_name}"

    return ComponentInfo(
        type=new_type,
        abspath=os.path.join(parent_info.abspath, new_name),
        number=new_number,
        number_data=None,
    )
