import rola
import miner
import data_manager
import os
import os.path
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository import Gst
import mutagen
from mutagen.id3 import ID3



def play_song(caller, tree_selection, PLAYER):
    try:
        (model, iter) = tree_selection.get_selected()
        path = model.get_value(iter,4)
    except:
        return

    if PLAYER[1] == False or PLAYER[2] != path:
        PLAYER[2] = path
        path = path.replace(" ", "\ ")
        if PLAYER[0] != None:
            PLAYER[0].set_state(Gst.State.NULL)
        pipeline = "filesrc location=" + path + " ! decodebin ! audioconvert ! autoaudiosink"
        player = Gst.parse_launch(pipeline)
        PLAYER[0] = player
        player.set_state(Gst.State.PLAYING)
        PLAYER[1] = True
    else :
        PLAYER[0].set_state(Gst.State.PLAYING)


def pause_song(caller, PLAYER):
    try:
        player = PLAYER[0]
        player.set_state(Gst.State.PAUSED)
    except:
        pass

#Hides an specific window
def hide_window(window, event):
    window.hide()
    return True


#Responds to a selected row in TreeView.
def selection(tree_selection, title_label, album_label, performer_label, imageview) :
    (model, iter) = tree_selection.get_selected()
    title = model.get_value(iter,0)
    album = model.get_value(iter,1)
    performer = model.get_value(iter,2)
    path = model.get_value(iter,4)

    title_label.set_text(title)
    album_label.set_text(album)
    performer_label.set_text(performer)

    audio = ID3(path)
    file = mutagen.File(path)
    try:
        artwork_data = file.tags['APIC:'].data
        loader = GdkPixbuf.PixbufLoader.new()
        loader.set_size(120, 120)
        loader.write(artwork_data)
        loader.close()
        pixbuf = loader.get_pixbuf()
        imageview.set_from_pixbuf(pixbuf)
    except:
        try:
            artwork_data = file.tags['APIC:'].data
            loader = GdkPixbuf.PixbufLoader.new_with_type('jpg')
            loader.set_size(120, 120)
            loader.write(artwork_data)
            loader.close()
            pixbuf = loader.get_pixbuf()
            imageview.set_from_pixbuf(pixbuf)
        except:
            imageview.set_from_file("resources/music.png")


#Mining process
def mine(trigger, data_access_object, miner, treeview):

    listmodel = Gtk.ListStore(str, str, str, str, str)
    rolas_representation = []

    if os.path.isfile("rolas.db"):
        os.remove("rolas.db")
        data_access_object.create_database()
        miner_object.mine()
        rolas = miner_object.get_rolas()
        albums = miner_object.get_albums()
        performers = miner_object.get_performers()
        data_access_object.populate_database(rolas = rolas ,
                                             performers = performers,
                                             albums = albums)
        db_rolas = data_access_object.get_rolas()
        db_albums = data_access_object.get_albums()
        db_performers = data_access_object.get_performers()
        for rola in db_rolas.values():
            representation = []
            representation.append(rola.get_title())
            representation.append(
                data_access_object.get_album(rola.get_album_id())[2])
            representation.append(
                data_access_object.get_performer(rola.get_performer_id())[2])
            representation.append(rola.get_genre())
            representation.append(rola.get_path())
            rolas_representation.append(representation)

    else :
        data_access_object.create_database()
        miner_object.mine()
        rolas = miner_object.get_rolas()
        albums = miner_object.get_albums()
        performers = miner_object.get_performers()
        data_access_object.populate_database(rolas = rolas ,
                                             performers = performers,
                                             albums = albums)
        db_rolas = data_access_object.get_rolas()
        db_albums = data_access_object.get_albums()
        db_performers = data_access_object.get_performers()
        for rola in db_rolas.values():
            representation = []
            representation.append(rola.get_title())
            representation.append(
                data_access_object.get_album(rola.get_album_id())[2])
            representation.append(
                data_access_object.get_performer(rola.get_performer_id())[2])
            representation.append(rola.get_genre())
            representation.append(rola.get_path())
            rolas_representation.append(representation)
    for item in rolas_representation :
        listmodel.append(item)
    treeview.set_model(listmodel)

if __name__ == "__main__" :

    PLAYER = []
    PLAYER.append(None)
    PLAYER.append(False)
    PLAYER.append("")

    #Initializes gstreamer
    Gst.init(None)

    #Gets the path to HOME/Music
    home = os.getenv("HOME")
    path = str(home + "/Music")

    #The rolas representation for the TreeView
    rolas_representation = []

    #Creates the miner
    miner_object = miner.Miner(path)
    miner_object.mine()

    #Gets the information from the tags
    rolas = miner_object.get_rolas()
    albums = miner_object.get_albums()
    performers = miner_object.get_performers()

    #Creates the DAO
    data_access_object = data_manager.Data_manager("", "rolas.db")

    #Fills the database
    if os.path.isfile("rolas.db"):
        os.remove("rolas.db")
        data_access_object.create_database()
        data_access_object.populate_database(rolas = rolas ,
                                             performers = performers,
                                             albums = albums)
        db_rolas = data_access_object.get_rolas()
        db_albums = data_access_object.get_albums()
        db_performers = data_access_object.get_performers()
        for rola in db_rolas.values():
            representation = []
            representation.append(rola.get_title())
            representation.append(
                data_access_object.get_album(rola.get_album_id())[2])
            representation.append(
                data_access_object.get_performer(rola.get_performer_id())[2])
            representation.append(rola.get_genre())
            representation.append(rola.get_path())
            rolas_representation.append(representation)

    else :
        data_access_object.create_database()
        data_access_object.populate_database(rolas = rolas ,
                                             performers = performers,
                                             albums = albums)
        db_rolas = data_access_object.get_rolas()
        db_albums = data_access_object.get_albums()
        db_performers = data_access_object.get_performers()
        for rola in db_rolas.values():
            representation = []
            representation.append(rola.get_title())
            representation.append(
                data_access_object.get_album(rola.get_album_id())[2])
            representation.append(
                data_access_object.get_performer(rola.get_performer_id())[2])
            representation.append(rola.get_genre())
            representation.append(rola.get_path())
            rolas_representation.append(representation)



    builder = Gtk.Builder()
    builder.add_from_file("resources/main.glade")
    about_builder = Gtk.Builder()
    about_builder.add_from_file("resources/about.glade")
    about_dialog = about_builder.get_object("about_dialog")
    about_dialog.connect("delete-event", hide_window)
    about_dialog.connect("destroy", hide_window)

    columns = ["Title",
               "Album",
               "Performer",
               "Genre",
               "Path"]

    rolas_liststore = builder.get_object("rolas_liststore")
    for element in rolas_representation:
        rolas_liststore.append(element)

    treeview = builder.get_object("treeview")

    handlers = {
        "exit": Gtk.main_quit,
        "mine": (mine, data_access_object, miner_object, treeview),
        "about": (lambda widget : about_dialog.show())
    }
    builder.connect_signals(handlers)


    for i, column in enumerate(columns):
        # cellrenderer to render the text
        cell = Gtk.CellRendererText()
        # the column is created
        col = Gtk.TreeViewColumn(column, cell, text=i)
        # and it is appended to the treeview
        if column == "Path":
            col.set_visible(False)
        treeview.append_column(col)

    title_label = builder.get_object("title_label")
    album_label = builder.get_object("album_label")
    performer_label = builder.get_object("performer_label")
    imageview = builder.get_object("imageview")


    tree_selection = treeview.get_selection()
    tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
    tree_selection.connect("changed", selection, title_label, album_label, performer_label, imageview)


    play_button = builder.get_object("play_button")
    play_button.connect("clicked", play_song, tree_selection, PLAYER)

    pause_button = builder.get_object("pause_button")
    pause_button.connect("clicked", pause_song, PLAYER)




    window = builder.get_object("main_window")
    window.show_all()


    Gtk.main()







'''

    from gi.repository import Pango
import sys




class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="My Phone Book", application=app)
        self.set_default_size(250, 100)
        self.set_border_width(10)

        # for each column
        for i, column in enumerate(columns):
            # cellrenderer to render the text
            cell = Gtk.CellRendererText()
            # the text in the first column should be in boldface
            if i == 0:
                cell.props.weight_set = True
                cell.props.weight = Pango.Weight.BOLD
            # the column is created
            col = Gtk.TreeViewColumn(column, cell, text=i)
            # and it is appended to the treeview
            view.append_column(col)

        # when a row is selected, it emits a signal
        view.get_selection().connect("changed", self.on_changed)

        # the label we use to show the selection
        self.label = Gtk.Label()
        self.label.set_text("")

        # a grid to attach the widgets
        grid = Gtk.Grid()
        grid.attach(view, 0, 0, 1, 1)
        grid.attach(self.label, 0, 1, 1, 1)

        # attach the grid to the window
        self.add(grid)

    def on_changed(self, selection):
        # get the model and the iterator that points at the data in the model
        (model, iter) = selection.get_selected()
        # set the label to a new value depending on the selection
        self.label.set_text("\n %s %s %s" %
                            (model[iter][0],  model[iter][1], model[iter][2]))
        return True


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)

'''
