import os
import os.path
import threading
import time

#imports the DAO
from .data_manager import DataManager
#imports the miner
from .miner import Miner
#imports the compiler for searchs inside the program
from .search_compiler import SearchCompiler
#imports rola class
from .rola import Rola
#imports tag window controller
from .tag_window_controller import TagWindowController

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
#import Gtk, GLib, GdkPixbuf, Gstreamer modules
from gi.repository import Gtk, GdkPixbuf, Gst, GLib

#imports mutagen module
import mutagen
#imports ID3 tags module from mutagen
from mutagen.id3 import ID3

class MainWindowController:

    #Global list for rolas representation
    data_list = []

    #Main Window Controller constructor
    def __init__(self):
        self.first_run = True
        self.default_database = False

        home = os.getenv("HOME")
        path = str(home + "/Music")
        self.miner = Miner(path)
        self.data_manager = DataManager("", "rolas.db")
        self.search_compiler = SearchCompiler()

        self.rolas_representation = []
        self.music_player = []
        self.music_player.append(None)
        self.music_player.append(False)
        self.music_player.append("")

        self.tag_window_controller = TagWindowController()

        self.builder = Gtk.Builder()
        self.builder.add_from_file("resources/main.glade")
        self.main_window = self.builder.get_object("main_window")

        self.liststore = self.builder.get_object("liststore")
        self.filter = self.liststore.filter_new()
        self.treeview = self.builder.get_object("treeview")
        self.treeview.set_model(self.filter)

        self.title_label = self.builder.get_object("title_label")
        self.album_label = self.builder.get_object("album_label")
        self.performer_label = self.builder.get_object("performer_label")
        self.imageview = self.builder.get_object("imageview")

        self.searchentry = self.builder.get_object("searchentry")

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
            "mine": (self.on_load_button_clicked),
            "about": (lambda widget : self.about_window.show()),
            "tag": (lambda widget : self.trigger_tag_window()),
            "search" : (self.on_search_entry_activated)
        }
        self.builder.connect_signals(handlers)

        self.tree_selection = self.treeview.get_selection()
        self.tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.tree_selection.connect("changed", self.on_selected_row)

        play_button = self.builder.get_object("play_button")
        play_button.connect("clicked", self.play_song)

        pause_button = self.builder.get_object("pause_button")
        pause_button.connect("clicked", self.pause_song)

        self.shown_rows = []

    def search_filter_func(self, model, iter, data):
        if self.shown_rows == [] :
            return True
        else:
            return model[iter][5] in self.shown_rows

    #Method that hides an specific window received as argument
    def hide_window(self, window, event):
        window.hide()
        return True

    # Method that plays a song using Gstreamer
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
            pipeline = "filesrc location=" + path + \
                       " ! decodebin ! audioconvert ! autoaudiosink"
            player = Gst.parse_launch(pipeline)
            self.music_player[0] = player
            player.set_state(Gst.State.PLAYING)
            self.music_player[1] = True
        else :
            self.music_player[0].set_state(Gst.State.PLAYING)

    # Method that pauses a song using Gstreamer
    def pause_song(self, caller):
        try:
            player = self.music_player[0]
            player.set_state(Gst.State.PAUSED)
        except:
            pass

    #Loads the music library when the "load" button is clicked
    def on_load_button_clicked(self, caller):
        if os.path.isfile("rolas.db"):
            os.remove("rolas.db")
            self.run_load_music_task(self.loading_window)
        else :
            self.run_load_music_task(self.loading_window)

    #Loads the music library when the "load" button is clicked
    def on_search_entry_activated(self, caller):
        search = self.searchentry.get_text()
        if search == "":
            self.shown_rows = []
            self.filter.refilter()
        else:
            command = self.search_compiler.compile(search)
            identifiers = self.data_manager.execute_and_get_ids(command)
            self.shown_rows = identifiers
            self.filter.refilter()
            self.searchentry.set_text("")

    # Gets the music information, while shows an loading window
    def run_load_music_task(self, loading_window):
        loading_window.show()

        def thread_run():
            fetch_info = self.fetch_info()
            GLib.idle_add(cleanup, fetch_info)

        def cleanup(fetch_info):
            loading_window.hide()
            thread.join()
            rolas_representation_list = fetch_info
            listmodel = Gtk.ListStore(str, str, str, str, str, int)
            for item in rolas_representation_list :
                listmodel.append(item)
            self.filter = listmodel.filter_new()
            self.filter.set_visible_func(self.search_filter_func)
            self.treeview.set_model(self.filter)

        thread = threading.Thread(target = thread_run)
        thread.start()

    # Retrieves the music info either only from the database or from both
    # the database and the miner object.
    def fetch_info(self):
        if self.default_database:
            self.default_database = False
        else :
            self.data_manager.create_database()
            self.mine()
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

    # Mines from the Music directory, and updates the loading window label
    # to show the actual progress
    def mine(self):
        def set_label_text(text):
            self.loading_label.set_text(text)
        self.miner.setup()
        self.miner.walk()
        for path in self.miner.get_paths():
            self.miner.mine(path)
            GLib.idle_add(set_label_text,
                          (str(self.miner.get_processed_files()) + " / " +
                           str(self.miner.get_total_files()) ))
        GLib.idle_add(set_label_text, "Loading music ...")
        self.rolas = self.miner.get_rolas()
        self.albums = self.miner.get_albums()
        self.performers = self.miner.get_performers()
        self.search_compiler.update(self.performers, self.albums)

    #Responds to a selected row signal in TreeView.
    def on_selected_row(self, caller) :
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
            tags = mutagen.mp3.Open(path)
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
                artwork_exists = False
                for tag in tags:
                    if tag.startswith("APIC"):
                        artwork_data = tags[tag].data
                        artwork_exists = True
                        break
                if artwork_exists:
                    loader = GdkPixbuf.PixbufLoader.new()
                    loader.set_size(120, 120)
                    loader.write(artwork_data)
                    loader.close()
                    pixbuf = loader.get_pixbuf()
                    self.imageview.set_from_pixbuf(pixbuf)
                else:
                    self.imageview.set_from_file("resources/music.png")
            except:
                self.imageview.set_from_file("resources/music.png")

    #Launches an tag editro window, with the selected row info from the treeview
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

    #Starts the Main Window Controller object.
    def start(self):
        Gst.init(None)
        self.mine()
        self.main_window.show_all()

        #Fills the database
        if os.path.isfile("rolas.db"):
            self.default_database = True
            self.run_load_music_task(self.loading_window)
        else :
            self.run_load_music_task(self.loading_window)

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
