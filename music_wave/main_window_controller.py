import rola
import miner
import data_manager
import os
import os.path
import gi
from gi.repository import Gtk

if __name__ == "__main__" :
    gi.require_version('Gtk', '3.0')
    home = os.getenv("HOME")
    path = str(home + "/Music")

    rolas_representation = []

    miner_object = miner.Miner(path)
    miner_object.mine()

    rolas = miner_object.get_rolas()
    albums = miner_object.get_albums()
    performers = miner_object.get_performers()

    data_access_object = data_manager.Data_manager("", "rolas.db")

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
            rolas_representation.append(representation)

    class Handler:
        def mine(self, *args):
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
                    rolas_representation.append(representation)

        def exit(self, *args):
            Gtk.main_quit()


    builder = Gtk.Builder()
    builder.add_from_file("resources/main.glade")
    builder.connect_signals(Handler())

    columns = ["Title",
               "Album",
               "Performer",
               "Genre"]

    rolas_liststore = builder.get_object("rolas_liststore")
    for element in rolas_representation:
        rolas_liststore.append(element)

    treeview = builder.get_object("treeview")


    for i, column in enumerate(columns):
        # cellrenderer to render the text
        cell = Gtk.CellRendererText()
        # the column is created
        col = Gtk.TreeViewColumn(column, cell, text=i)
        # and it is appended to the treeview
        treeview.append_column(col)

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
