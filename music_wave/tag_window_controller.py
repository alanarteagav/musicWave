from music_wave.data_manager import DataManager

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TagWindowController:
    def __init__(self):
        self.data_manager = DataManager("", "rolas.db")

        self.id = 0
        self.album = ""
        self.performer = ""
        self.path = ""
        self.builder = Gtk.Builder()
        self.builder.add_from_file("resources/tag.glade")
        self.tag_window = self.builder.get_object("tag_window")
        self.title_entry = self.builder.get_object("title_entry")
        self.genre_entry = self.builder.get_object("genre_entry")
        self.track_entry = self.builder.get_object("track_entry")
        self.year_entry = self.builder.get_object("year_entry")

        self.discard_button = self.builder.get_object("discard_button")
        self.discard_button.connect("clicked", self.hide_window_with_button)

        self.apply_button = self.builder.get_object("apply_button")
        self.apply_button.connect("clicked", self.apply_changes)

        self.tag_window.connect("delete-event", self.hide_window)
        self.tag_window.connect("destroy", self.hide_window)

        self.func = lambda : None
        self.treemodel = None
        self.treeiter = None

    def hide_window(self, window, event):
        window.hide()
        return True

    def hide_window_with_button(self, caller):
        self.tag_window.hide()
        return True

    def apply_changes(self, caller):
        title = self.title_entry.get_text()
        genre = self.genre_entry.get_text()
        track = self.track_entry.get_text()
        year = self.year_entry.get_text()
        self.data_manager.update_rola(self.id, title, track, year, genre)
        self.tag_window.hide()
        values = [title, self.album, self.performer, genre, self.path, self.id]
        self.treemodel.set_row(self.treeiter, values)
        return True

    def set_id(self, id):
        self.id = id
    def set_album(self, album):
        self.album = album
    def set_performer(self, performer):
        self.performer = performer
    def set_path(self, path):
        self.path = path

    def set_lambda(self, func):
        self.func = func

    def set_treemodel(self, treemodel):
        self.treemodel = treemodel

    def set_treeiter(self, treeiter):
        self.treeiter = treeiter

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
