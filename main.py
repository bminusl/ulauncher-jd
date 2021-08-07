from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


class JohnnyDecimalExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        data_keys = ["icon", "name", "description"]
        data_values = [
            ("images/area.png", "Areas", "Perform actions on Areas"),
            ("images/category.png", "Categories", "Perform actions on Categories"),
            ("images/id.png", "IDs (items)", "Perform actions on Items"),
        ]
        items = [
            ExtensionResultItem(
                **dict(zip(data_keys, values)),
                on_enter=HideWindowAction(),
            )
            for values in data_values
        ]
        return RenderResultListAction(items)


if __name__ == '__main__':
    JohnnyDecimalExtension().run()
