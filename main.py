import os

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.RenderResultListAction import (
    RenderResultListAction,
)
from ulauncher.api.shared.event import (
    ItemEnterEvent,
    KeywordQueryEvent,
    PreferencesEvent,
    PreferencesUpdateEvent,
)

from ulauncher_jd import ComponentInfo, preferences
from ulauncher_jd.filesystem import find, next_available_component, search
from ulauncher_jd.items import create_component_item, open_component_item


class JohnnyDecimalExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())

    def get_default_basedir_info(self, basedir):
        return ComponentInfo(None, basedir, None, None)


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):

        # XXX: should this be here?
        os.makedirs(preferences["basedir"], exist_ok=True)

        query = event.query.split(" ")
        kw = query[0]
        user_text = " ".join(query[1:])

        items = []

        if kw == extension.preferences["jd_kw"]:
            for component_info in search(user_text):
                items.append(open_component_item(component_info))
        elif kw == extension.preferences["jdn_kw"]:

            if len(query) >= 2:
                # BBB: walrus operator
                #
                # The 2nd argument (query[1]) is potentially a parent number
                # i.e. `XX-XX` (area) or `XX` (category)
                parent_info = find(query[1])
                if parent_info and parent_info.type != "id":
                    # XXX: in 2 steps because black adds ' ' before `:`
                    x = len(query[1]) + 1
                    new_name = user_text[x:].strip()

                    items.append(
                        create_component_item(
                            new_name,
                            next_available_component(new_name, parent_info),
                            parent_info,
                        )
                    )

                items.append(
                    create_component_item(
                        user_text,
                        next_available_component(
                            user_text, preferences["basedir_info"]
                        ),
                        preferences["basedir_info"],
                    )
                )

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        type = data["type"]

        if type == "mkdir":
            os.mkdir(data["abspath"])

        return DoNothingAction()


class PreferencesEventListener(EventListener):
    def on_event(self, event, extension):
        preferences.update(event.preferences)
        preferences["basedir"] = os.path.expanduser(
            os.path.expandvars(preferences["basedir"])
        )
        preferences["basedir_info"] = extension.get_default_basedir_info(
            preferences["basedir"]
        )


class PreferencesUpdateEventListener(EventListener):
    def on_event(self, event, extension):
        preferences[event.id] = event.new_value
        if event.id == "basedir":
            preferences["basedir"] = os.path.expanduser(
                os.path.expandvars(preferences["basedir"])
            )
            preferences["basedir_info"] = extension.get_default_basedir_info(
                preferences["basedir"]
            )


if __name__ == "__main__":
    JohnnyDecimalExtension().run()
