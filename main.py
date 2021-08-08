from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.RenderResultListAction import (
    RenderResultListAction,
)
from ulauncher.api.shared.event import KeywordQueryEvent

from ulauncher_jd.format import match_type
from ulauncher_jd.items import create_component_item, open_component_item
from ulauncher_jd.search import search


class JohnnyDecimalExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):

        query = event.query.split(" ")
        kw = query[0]
        user_text = " ".join(query[1:])

        items = []

        if kw == extension.preferences["jd_kw"]:
            for item_args in sorted(search(user_text)):
                items.append(open_component_item(*item_args))
        elif kw == extension.preferences["jdn_kw"]:

            if len(query) >= 2:
                # BBB: walrus operator
                #
                # The 2nd argument is potentially a parent number
                # i.e. `XX-XX` (area) or `XX` (category)
                parent_number = query[1]
                parent_type = match_type(parent_number)
                if parent_type:
                    child_type = {"area": "category", "category": "id"}[
                        parent_type
                    ]
                    # XXX: in 2 steps because black add ' ' before `:`
                    x = len(parent_number) + 1
                    user_text = user_text[x:]
                    items.append(
                        create_component_item(
                            child_type,
                            user_text,
                            parent_info=(parent_type, parent_number),
                        )
                    )
                else:
                    items.append(create_component_item("area", user_text))

        return RenderResultListAction(items)


if __name__ == "__main__":
    JohnnyDecimalExtension().run()
