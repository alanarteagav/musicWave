import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Handler():
    def quit(self, *args):
        Gtk.main_quit()

    def mineMusic(self, *args):
        Gtk.main_quit()

builder = Gtk.Builder()
builder.add_from_file("resources/main.glade")
builder.connect_signals(Handler())

window = builder.get_object("main_window")
window.show_all()

Gtk.main()
