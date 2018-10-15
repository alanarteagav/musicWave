import os
import os.path
import threading
import time

import data_manager
import miner
import rola

import tag_window_controller

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, GdkPixbuf, Gst, GLib

import mutagen
from mutagen.id3 import ID3

class MainWindowController:

    data_list = []

    def __init__(self):

        self.first_run = True
        self.default_database = False

        home = os.getenv("HOME")
        path = str(home + "/Music")
        self.miner = miner.Miner(path)
        self.data_manager = data_manager.Data_manager("", "rolas.db")

        self.rolas_representation = []
        self.music_player = []
        self.music_player.append(None)
        self.music_player.append(False)
        self.music_player.append("")

        self.tag_window_controller = tag_window_controller.TagWindowController()

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
        self.loading_label = loading_builder.get_object("loading_label")

        about_builder = Gtk.Builder()
        about_builder.add_from_file("resources/about.glade")
        self.about_window = about_builder.get_object("about_window")

        tag_builder = Gtk.Builder()
        tag_builder.add_from_file("resources/tag.glade")

        self.columns = ["Title", "Album", "Performer", "Genre", "Path", 0]

        handlers = {
            "exit": Gtk.main_quit,
            "mine": (self.mine),
            "about": (lambda widget : self.about_window.show()),
            "tag": (lambda widget : self.trigger_tag_window())
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
        if self.default_database:
            self.default_database = False
        else :
            self.data_manager.create_database()
            self.mine2()
            self.data_manager.populate_database(rolas = self.rolas ,
                                                performers = self.performers,
                                                albums = self.albums)
        db_rolas = self.data_manager.get_rolas()
        db_albums = self.data_manager.get_albums()
        db_performers = self.data_manager.get_performers()
        rolas_representation = []
        for rola in db_rolas.values():
            representation = []
            representation.append(rola.get_title().replace("´", "'"))
            representation.append(
                self.data_manager.get_album(rola.get_album_id())[2])
            representation.append(
                self.data_manager.get_performer(rola.get_performer_id())[2])
            representation.append(rola.get_genre())
            representation.append(rola.get_path())
            representation.append(rola.get_id())
            rolas_representation.append(representation)
        if self.first_run:
            self.data_list = rolas_representation
        else:
            return rolas_representation

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

    def close_window(self, window, event):
        window.close()
        return True


    #Responds to a selected row in TreeView.
    def on_select_row(self, caller) :
        try:
            (model, iter) = self.tree_selection.get_selected()
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
                loader = GdkPixbuf.PixbufLoader.new_with_type('JPG')
                loader.set_size(120, 120)
                loader.write(artwork_data)
                loader.close()
                pixbuf = loader.get_pixbuf()
                self.imageview.set_from_pixbuf(pixbuf)
            except:
                self.imageview.set_from_file("resources/music.png")


    def load_music(self, loading_window):
        loading_window.show()


        def thread_run():
            # call heavy here
            heavy_ret = self.fetch_info()
            GLib.idle_add(cleanup, heavy_ret)

        def cleanup(heavy_ret):
            loading_window.hide()
            thread.join()
            data_list = heavy_ret
            listmodel = Gtk.ListStore(str, str, str, str, str, int)
            for item in data_list :
                listmodel.append(item)
            self.treeview.set_model(listmodel)

        # start "heavy" in a separate thread and immediately
        # return to mainloop
        thread = threading.Thread(target = thread_run)
        thread.start()


    def set_label_text(self, text):
        self.loading_label.set_text(text)

    #Mining process
    def mine(self, caller):

        if os.path.isfile("rolas.db"):
            os.remove("rolas.db")
            self.load_music(self.loading_window)

        else :
            self.load_music(self.loading_window)

    def mine2(self):
        self.miner.setup()
        self.miner.walk()
        for path in self.miner.get_paths():
            self.miner.mine(path)
            GLib.idle_add(self.set_label_text,
                          (str(self.miner.get_progress()) + " / " +
                           str(self.miner.get_total_files()) ))
        GLib.idle_add(self.set_label_text, "Loading music ...")
        self.rolas = self.miner.get_rolas()
        self.albums = self.miner.get_albums()
        self.performers = self.miner.get_performers()

    def trigger_tag_window(self):
            (model, iter) = self.tree_selection.get_selected()
            id = model.get_value(iter,5)
            rola = self.data_manager.get_rola(id)
            title = rola[4]
            track = str(rola[5])
            year = str(rola[6])
            genre = rola[7]
            self.tag_window_controller.set_title_entry_text(title)
            self.tag_window_controller.set_track_entry_text(track)
            self.tag_window_controller.set_year_entry_text(year)
            self.tag_window_controller.set_genre_entry_text(genre)
            self.tag_window_controller.show_window()

    def start(self):
        Gst.init(None)
        self.mine2()
        self.main_window.show_all()

        #Fills the database
        if os.path.isfile("rolas.db"):
            self.default_database = True
            self.fetch_info()
        else :
            self.fetch_info()

        self.first_run = False

        self.about_window.connect("delete-event", self.hide_window)
        self.about_window.connect("destroy", self.hide_window)

        for representation in self.data_list:
            self.liststore.append(representation)

        for index, column in enumerate(self.columns):
            # cellrenderer to render the text
            cell = Gtk.CellRendererText()
            # the column is created
            col = Gtk.TreeViewColumn(column, cell, text=index)
            # and it is appended to the treeview
            if column == "Path" or column == 0:
                col.set_visible(False)
            self.treeview.append_column(col)
