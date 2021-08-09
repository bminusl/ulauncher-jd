import os

from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from ulauncher_jd.filesystem import next_available_component


def display_type(type):
    return {"area": "Area", "category": "Category", "id": "ID"}[type]


def open_component_item(component_info):
    return ExtensionResultItem(
        icon=f"images/{component_info.type}.png",
        name=os.path.basename(component_info.abspath),
        description=f"Open the {display_type(component_info.type)}",
        on_enter=OpenAction(component_info.abspath),
    )


def create_component_item(new_name, parent_info):

    component_info = next_available_component(new_name, parent_info)

    display_name = os.path.basename(component_info.abspath)
    description = f"Create a new {display_type(component_info.type)}"
    if parent_info.type is not None:
        description += f' in {display_type(parent_info.type)} "{display_name}"'

    # BBB: walrus operator
    if new_name:
        action = None
    else:
        display_name = '<span style="italic">Please enter a name</span>'
        action = None

    return ExtensionResultItem(
        icon=f"images/{component_info.type}.png",
        name=display_name,
        description=description,
        on_enter=action,
        highlightable=False,
    )
