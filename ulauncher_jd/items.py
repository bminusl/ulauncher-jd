import os

from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from ulauncher_jd.search import find_name


def display_type(type):
    return {"area": "Area", "category": "Category", "id": "ID"}[type]


def open_component_item(type, abspath):
    return ExtensionResultItem(
        icon=f"images/{type}.png",
        name=os.path.basename(abspath),
        description=f"Open the {display_type(type)}",
        on_enter=OpenAction(abspath),
    )


def create_component_item(type, name, parent_info=None):
    description = f"Create a new {display_type(type)}"
    if parent_info is not None:
        parent_type, parent_number = parent_info
        parent_name = find_name(parent_number)
        description += f' in {display_type(parent_type)} "{parent_name}"'

    return ExtensionResultItem(
        icon=f"images/{type}.png",
        name=name,
        description=description,
        on_enter=None,
    )
