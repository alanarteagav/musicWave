import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TagWindowController:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("resources/tag.glade")
        self.tag_window = self.builder.get_object("tag_window")
        self.title_entry = self.builder.get_object("title_entry")
        self.genre_entry = self.builder.get_object("genre_entry")
        self.track_entry = self.builder.get_object("track_entry")
        self.year_entry = self.builder.get_object("year_entry")
        self.tag_window.connect("delete-event", self.hide_window)
        self.tag_window.connect("destroy", self.hide_window)

    def hide_window(self, window, event):
        window.hide()
        return True

    def set_title_entry_text(self, title):
        self.title_entry.set_text(title)

    def set_genre_entry_text(self, genre):
        self.genre_entry.set_text(genre)

    def set_track_entry_text(self, track):
        self.track_entry.set_text(track)

    def set_year_entry_text(self, year):
        self.year_entry.set_text(year)

    def get_title_entry_text(self, title):
        self.title_entry.get_text(title)

    def get_genre_entry_text(self, genre):
        self.genre_entry.get_text(genre)

    def get_track_entry_text(self, track):
        self.track_entry.get_text(track)

    def get_year_entry_text(self, year):
        self.year_entry.get_text(year)

    def show_window(self):
        self.tag_window.show()
