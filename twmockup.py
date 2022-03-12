import urwid
from dataclasses import dataclass, asdict, field, InitVar, replace
from random_word import RandomWords
import tw2022

rw = RandomWords()

class ListItem(urwid.WidgetWrap):
    def __init__(self, item):
        self.content = item
        name = item["name"]
        t = urwid.AttrWrap(urwid.Text(name), "item", "item_selected")
        urwid.WidgetWrap.__init__(self, t)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key

class ListView(urwid.WidgetWrap):

    def __init__(self):
        urwid.register_signal(self.__class__, ['show_details'])
        self.walker = urwid.SimpleFocusListWalker([])

        lb = urwid.ListBox(self.walker)

        urwid.WidgetWrap.__init__(self, lb)

    def modified(self):
        focus_w, _ = self.walker.get_focus()
        urwid.emit_signal(self, 'show_details', focus_w.content)

    def set_data(self, items):
        item_widgets = [ListItem(i) for i in items]
        urwid.disconnect_signal(self.walker, 'modified', self.modified)

        while len(self.walker) > 0:
            self.walker.pop()

        self.walker.extend(item_widgets)
        urwid.connect_signal(self.walker, "modified", self.modified)
        self.walker.set_focus(0)

class DetailView(urwid.WidgetWrap):

    def __init__(self):
        t = urwid.Text("")
        urwid.WidgetWrap.__init__(self, t)

    def set_fields(self, item):


class App(object):

    def unhandled_input(self, key):
        if key in ('q', 'Q',):
            raise urwid.ExitMainLoop()

    def __init__(self):

        self.palette = {
            ('bg', 'black', 'white'),
            ('log', 'blue', 'white'),
            ('list', 'dark blue', 'white'),
            ('status', 'white, bold', 'dark red'),
            ('gametime', 'white, bold', 'dark red'),
        }

        self.list_view = ListView()
        self.log_view = LogView()


