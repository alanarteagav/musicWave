import os
import os.path
import threading
import time

import data_manager
import miner
import rola

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, GdkPixbuf, Gst, GLib

import mutagen
from mutagen.id3 import ID3

class MainWindowController:
    def __init__(self):
        home = os.getenv("HOME")
        path = str(home + "/Music")
        self.miner = miner.Miner(path)
        self.data_manager = data_manager.Data_manager("", "rolas.db")
        self.rolas_representation = []
        self.music_player = []
        self.music_player.append(None)
        self.music_player.append(False)
        self.music_player.append("")

        self.builder = Gtk.Builder()
        self.builder.add_from_file("resources/main.glade")
        self.main_window = self.builder.get_object("main_window")

        self.liststore = self.builder.get_object("liststore")
        self.treeview = self.builder.get_object("treeview")

        self.title_label = self.builder.get_object("title_label")
        self.album_label = self.builder.get_object("album_label")
        self.performer_label = self.builder.get_object("performer_label")
        self.imageview = self.builder.get_object("imageview")

        loading_builder = Gtk.Builder()
        loading_builder.add_from_file("resources/loading.glade")
        self.loading_window = loading_builder.get_object("loading_window")

        about_builder = Gtk.Builder()
        about_builder.add_from_file("resources/about.glade")
        self.about_window = about_builder.get_object("about_window")

        self.columns = ["Title", "Album", "Performer", "Genre", "Path"]

        handlers = {
            "exit": Gtk.main_quit,
            "mine": (self.mine),
            "about": (lambda widget : self.about_window.show())
        }
        self.builder.connect_signals(handlers)

        self.tree_selection = self.treeview.get_selection()
        self.tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.tree_selection.connect("changed", self.on_select_row)

        play_button = self.builder.get_object("play_button")
        play_button.connect("clicked", self.play_song)

        pause_button = self.builder.get_object("pause_button")
        pause_button.connect("clicked", self.pause_song)

    def fetch_info(self):
        self.loading_window.show()
        self.data_manager.create_database()
        self.data_manager.populate_database(rolas = self.rolas ,
                                             performers = self.performers,
                                             albums = self.albums)
        db_rolas = self.data_manager.get_rolas()
        db_albums = self.data_manager.get_albums()
        db_performers = self.data_manager.get_performers()
        for rola in db_rolas.values():
            representation = []
            representation.append(rola.get_title().replace("´", "'"))
            representation.append(
                self.data_manager.get_album(rola.get_album_id())[2])
            representation.append(
                self.data_manager.get_performer(rola.get_performer_id())[2])
            representation.append(rola.get_genre())
            representation.append(rola.get_path())
            self.rolas_representation.append(representation)
        print(hex(id(self.rolas_representation)))
        self.loading_window.hide()

    def play_song(self, caller):
        try:
            (model, iter) = self.tree_selection.get_selected()
            path = model.get_value(iter,4)
        except:
            return

        if self.music_player[1] == False or self.music_player[2] != path:
            self.music_player[2] = path
            path = path.replace(" ", "\ ")
            if self.music_player[0] != None:
                self.music_player[0].set_state(Gst.State.NULL)
            pipeline = "filesrc location=" + path + " ! decodebin ! audioconvert ! autoaudiosink"
            player = Gst.parse_launch(pipeline)
            self.music_player[0] = player
            player.set_state(Gst.State.PLAYING)
            self.music_player[1] = True
        else :
            self.music_player[0].set_state(Gst.State.PLAYING)


    def pause_song(self, caller):
        try:
            player = self.music_player[0]
            player.set_state(Gst.State.PAUSED)
        except:
            pass

    #Hides an specific window
    def hide_window(self, window, event):
        window.hide()
        return True


    #Responds to a selected row in TreeView.
    def on_select_row(self, caller) :
        try:
            (model, iter) = self.tree_selection.get_selected()
            self.play_song(caller)

            title = model.get_value(iter,0)
            album = model.get_value(iter,1)
            performer = model.get_value(iter,2)
            path = model.get_value(iter,4)

            self.title_label.set_text(title)
            self.album_label.set_text(album)
            self.performer_label.set_text(performer)

            audio = ID3(path)
            file = mutagen.File(path)
        except :
            return
        try:
            artwork_data = file.tags['APIC:'].data
            loader = GdkPixbuf.PixbufLoader.new()
            loader.set_size(120, 120)
            loader.write(artwork_data)
            loader.close()
            pixbuf = loader.get_pixbuf()
            self.imageview.set_from_pixbuf(pixbuf)
        except:
            try:
                artwork_data = file.tags['APIC:'].data
                loader = GdkPixbuf.PixbufLoader.new_with_type('jpg')
                loader.set_size(120, 120)
                loader.write(artwork_data)
                loader.close()
                pixbuf = loader.get_pixbuf()
                self.imageview.set_from_pixbuf(pixbuf)
            except:
                self.imageview.set_from_file("resources/music.png")


    #Mining process
    def mine(self, caller):
        listmodel = Gtk.ListStore(str, str, str, str, str)
        self.rolas_representation = []
        if os.path.isfile("rolas.db"):
            os.remove("rolas.db")
            self.fetch_info()
        else :
            self.fetch_info()
        for item in self.rolas_representation :
            listmodel.append(item)
        self.treeview.set_model(listmodel)

    def start(self):
        Gst.init(None)
        self.miner.mine()

        #Gets the information from the tags
        self.rolas = self.miner.get_rolas()
        self.albums = self.miner.get_albums()
        self.performers = self.miner.get_performers()

        self.main_window.show_all()

        print(hex(id(self.rolas_representation)))

        #Fills the database
        if os.path.isfile("rolas.db"):
            os.remove("rolas.db")
            self.fetch_info()
        else :
            self.fetch_info()


        self.about_window.connect("delete-event", self.hide_window)
        self.about_window.connect("destroy", self.hide_window)

        for representation in self.rolas_representation:
            self.liststore.append(representation)

        for index, column in enumerate(self.columns):
            # cellrenderer to render the text
            cell = Gtk.CellRendererText()
            # the column is created
            col = Gtk.TreeViewColumn(column, cell, text=index)
            # and it is appended to the treeview
            if column == "Path":
                col.set_visible(False)
            self.treeview.append_column(col)
