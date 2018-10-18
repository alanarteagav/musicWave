from .data_manager import DataManager

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AlbumWindowController:
    def __init__(self):
        self.data_manager = DataManager("", "rolas.db")

        self.id = 0
        self.old_name = ""
        self.builder = Gtk.Builder()
        self.builder.add_from_file("resources/album.glade")
        self.album_window = self.builder.get_object("album_window")
        self.name_entry = self.builder.get_object("name_entry")
        self.year_entry = self.builder.get_object("year_entry")

        self.discard_button = self.builder.get_object("discard_button")
        self.discard_button.connect("clicked", self.hide_window_with_button)

        self.apply_button = self.builder.get_object("apply_button")
        self.apply_button.connect("clicked", self.apply_changes)

        self.album_window.connect("delete-event", self.hide_window)
        self.album_window.connect("destroy", self.hide_window)

        self.filter = None

    def hide_window(self, window, event):
        window.hide()
        return True

    def hide_window_with_button(self, caller):
        self.album_window.hide()
        return True

    def apply_changes(self, caller):
        name = self.name_entry.get_text()
        year = self.year_entry.get_text()
        self.data_manager.update_album(self.id, name, year)
        self.album_window.hide()
        for row in self.filter:
            if row[1] == self.old_name:
                row[1] = name
        return True

    def set_id(self, id):
        self.id = id

    def set_old_name(self, old_name):
        self.old_name = old_name

    def set_filter(self, filter):
        self.filter = filter

    def set_name_entry_text(self, name):
        self.name_entry.set_text(name)

    def set_year_entry_text(self, year):
        self.year_entry.set_text(year)

    def show_window(self):
        self.album_window.show()
