import urwid
#from tw2022 import PlayerChar, Ship, Planet
import tw2022
from random_word import RandomWords

"""
Some test code to experiment with TUI
"""

rw = RandomWords()

testpc1 = tw2022.PlayerChar("Grant",
                        tw2022.startingFunds,
                        "Earth",
                        )



testship1 = tw2022.Ship("Titanic",
                    "RuPaul",
                    "Seattle",
                    "Drag Racer",
                    "A Class",
                    )

testplanet1 = tw2022.Planet("Mars",
                        tw2022.galaxy,
                        True,
                        "M",
                        )

def mk_ships(num):
    """
    Return a dict of arbitrary number of random ships
    """

    ship_dict = {}
    keys = range(num)

    for i in keys:
        rwsl = rw.get_random_words(limit=5)
        rwsa = tw.Ship(*rwsl)
        ship_dict[i] = [rwsa]
    return ship_dict

def menu_button(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def sub_menu(caption, choices):
    contents = menu(caption, choices)
    def open_menu(button):
        return top.open_box(contents)
    return menu_button([caption, u'...'], open_menu)

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def get_info(button):
    urwid.ListBox(urwid.SimpleFocusListWalker(body))
    response = urwid.Text([u'You chose ', button.label, u'\n'])
    done = menu_button(u'Ok', exit_program)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def rename(button):
    response = urwid.Text([u'You chose ', button.label, u'\n'])
    done = menu_button(u'Ok', exit_program)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def item_chosen(button):
    response = urwid.Text([u'You chose ', button.label, u'\n'])
    done = menu_button(u'Ok', exit_program)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def exit_program(button):
    raise urwid.ExitMainLoop()

menu_top = menu(u'Main Menu', [
    sub_menu(u'Assets', [
        sub_menu(u'Ships', [
            menu_button(u'Get Info', get_info),
            menu_button(u'Rename', rename),
        ]),
    ]),
    sub_menu(u'Locations', [
        sub_menu(u'Planets', [
            menu_button(u'Appearance', item_chosen),
        ]),
        menu_button(u'Space Stations', item_chosen),
    ]),
])

class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 4

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill(u'/'))
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=24, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        self.box_level += 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)

top = CascadingBoxes(menu_top)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
