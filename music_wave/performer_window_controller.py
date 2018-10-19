from .data_manager import DataManager

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PerformerWindowController:
    def __init__(self):
        self.data_manager = DataManager("", "rolas.db")

        self.type = "Unknown"
        self.adding_method = "New person"

        self.id = 0
        self.group_id = 0
        self.old_name = ""

        self.builder = Gtk.Builder()
        self.builder.add_from_file("resources/performer.glade")
        self.performer_window = self.builder.get_object("performer_window")
        self.add_window = self.builder.get_object("add_window")
        self.see_window = self.builder.get_object("see_window")
        self.liststore = self.builder.get_object("liststore")

        self.stage_entry = self.builder.get_object("stage_entry")
        self.real_entry = self.builder.get_object("real_entry")
        self.birth_entry = self.builder.get_object("birth_entry")
        self.death_entry = self.builder.get_object("death_entry")

        self.name_entry = self.builder.get_object("name_entry")
        self.start_entry = self.builder.get_object("start_entry")
        self.end_entry = self.builder.get_object("end_entry")

        self.stage_entry_new = self.builder.get_object("stage_entry_new")
        self.real_entry_new = self.builder.get_object("real_entry_new")
        self.birth_entry_new = self.builder.get_object("birth_entry_new")
        self.death_entry_new = self.builder.get_object("death_entry_new")

        self.comboboxtext = self.builder.get_object("comboboxtext")
        self.adding_combobox = self.builder.get_object("adding_combobox")
        self.builder.connect_signals({"adding_changed" : self.adding_changed,
                                      "type_changed" : self.change_type,
                                      "add_persons" : self.trigger_add_window,
                                      "see_persons" : self.trigger_see_window })

        self.stage_name_box = self.builder.get_object("stage_name_box")
        self.real_name_box = self.builder.get_object("real_name_box")
        self.birth_box = self.builder.get_object("birth_box")
        self.death_box = self.builder.get_object("death_box")

        self.name_box = self.builder.get_object("name_box")
        self.start_box = self.builder.get_object("start_box")
        self.end_box = self.builder.get_object("end_box")
        self.button_box = self.builder.get_object("button_box")

        self.stage_name_box_new = self.builder.get_object("stage_name_box_new")
        self.real_name_box_new = self.builder.get_object("real_name_box_new")
        self.birth_box_new = self.builder.get_object("birth_box_new")
        self.death_box_new = self.builder.get_object("death_box_new")
        self.persons_combobox = self.builder.get_object("persons_combobox")

        self.persons_treeview = self.builder.get_object("persons_treeview")

        self.see_button = self.builder.get_object("see_button")
        self.add_button = self.builder.get_object("add_button")


        self.discard_button = self.builder.get_object("discard_button")
        self.discard_button.connect("clicked", self.hide_window_with_button)

        self.apply_button = self.builder.get_object("apply_button")
        self.apply_button.connect("clicked", self.apply_changes)

        self.discard_button_add = self.builder.get_object("discard_button_add")
        self.discard_button_add.connect("clicked", self.hide_add_window_with_button)

        self.add_person_button = self.builder.get_object("add_person_button")
        self.add_person_button.connect("clicked", self.add_person)

        self.performer_window.connect("delete-event", self.hide_window)
        self.performer_window.connect("destroy", self.hide_window)

        self.add_window.connect("delete-event", self.hide_add_window)
        self.add_window.connect("destroy", self.hide_add_window)

        self.see_window.connect("delete-event", self.hide_window)
        self.see_window.connect("destroy", self.hide_window)

        self.filter = None

    def hide_window(self, window, event):
        window.hide()
        return True

    def hide_add_window(self, window, event):
        self.persons_combobox.remove_all()
        window.hide()
        return True

    def hide_window_with_button(self, caller):
        self.performer_window.hide()
        return True

    def hide_add_window_with_button(self, caller):
        self.persons_combobox.remove_all()
        self.add_window.hide()
        return True

    def change_type(self, caller):
        self.type = self.comboboxtext.get_active_text()
        if self.type == "Group":
            self.name_box.show()
            self.start_box.show()
            self.end_box.show()
            self.button_box.show()
            self.stage_name_box.hide()
            self.real_name_box.hide()
            self.birth_box.hide()
            self.death_box.hide()
        elif self.type == "Person":
            self.stage_name_box.show()
            self.real_name_box.show()
            self.birth_box.show()
            self.death_box.show()
            self.name_box.hide()
            self.start_box.hide()
            self.end_box.hide()
            self.button_box.hide()
        elif self.type == "Unknown":
            self.name_box.show()
            self.start_box.hide()
            self.end_box.hide()
            self.stage_name_box.hide()
            self.real_name_box.hide()
            self.birth_box.hide()
            self.death_box.hide()
            self.button_box.hide()
        return True

    def adding_changed(self, caller):
        self.type = self.adding_combobox.get_active_text()
        if self.type == "Existing person":
            self.stage_name_box_new.hide()
            self.real_name_box_new.hide()
            self.birth_box_new.hide()
            self.death_box_new.hide()
            self.persons_combobox.show()
            self.adding_method = "Existing person"
        elif self.type == "New person":
            self.stage_name_box_new.show()
            self.real_name_box_new.show()
            self.birth_box_new.show()
            self.death_box_new.show()
            self.persons_combobox.hide()
            self.adding_method = "New person"
        return True

    def clear_entries(self):
        self.stage_entry.set_text("")
        self.real_entry.set_text("")
        self.birth_entry.set_text("")
        self.death_entry.set_text("")
        self.name_entry.set_text("")
        self.start_entry.set_text("")
        self.end_entry.set_text("")

    def clear_add_window_entries(self):
        self.stage_entry_new.set_text("")
        self.real_entry_new.set_text("")
        self.birth_entry_new.set_text("")
        self.death_entry_new.set_text("")

    def apply_changes(self, caller):
        name = ""

        if self.type == "Unknown":
            name = self.name_entry.get_text()
            self.data_manager.update_performer(self.id, 2, name)
        elif self.type == "Person":
            stage_name = self.stage_entry.get_text()
            name = stage_name
            real_name = self.real_entry.get_text()
            birth_date = self.birth_entry.get_text()
            death_date = self.death_entry.get_text()
            if self.data_manager.is_unknown(self.id):
                self.data_manager.update_performer(self.id, 0, stage_name)
                self.data_manager.insert_person(stage_name, real_name, birth_date, death_date)
            elif self.data_manager.is_in_performers(stage_name, 0):
                self.data_manager.update_person(stage_name, real_name, birth_date, death_date)
        elif self.type == "Group":
            name = self.name_entry.get_text()
            start_date = self.start_entry.get_text()
            end_date = self.end_entry.get_text()
            if self.data_manager.is_unknown(self.id):
                self.data_manager.update_performer(self.id, 1, name)
                self.data_manager.insert_group(name, start_date, end_date)
            elif self.data_manager.is_in_performers(name, 1):
                self.data_manager.update_group(name, start_date, end_date)

        self.clear_entries()
        self.performer_window.hide()
        for row in self.filter:
            if row[2] == self.old_name:
                row[2] = name
        return True

    def add_person(self, caller):
        name = ""
        if self.adding_method == "New person":
            stage_name = self.stage_entry_new.get_text()
            name = stage_name
            real_name = self.real_entry_new.get_text()
            birth_date = self.birth_entry_new.get_text()
            death_date = self.death_entry_new.get_text()
            self.data_manager.insert_person(stage_name, real_name, birth_date, death_date)
            group = self.data_manager.get_group(self.name_entry.get_text())
            person = self.data_manager.get_person(name)
            self.data_manager.insert_in_group(person[0], group[0])

        elif self.adding_method == "Existing person":
            name = self.persons_combobox.get_active_text()
            group = self.data_manager.get_group(self.name_entry.get_text())
            person = self.data_manager.get_person(name)
            if self.data_manager.is_in_group(person[0], group[0]):
                pass
            else:
                self.data_manager.insert_in_group(person[0], group[0])

        self.clear_add_window_entries()
        self.persons_combobox.remove_all()
        self.add_window.hide()
        return True

    def set_id(self, id):
        self.id = id

    def set_type(self, type):
        self.type = type

    def set_old_name(self, old_name):
        self.old_name = old_name

    def set_filter(self, filter):
        self.filter = filter

    def set_stage_entry_text(self, stage):
        self.stage_entry.set_text(stage)
    def set_real_entry_text(self, real):
        self.real_entry.set_text(real)
    def set_birth_entry_text(self, birth):
        self.birth_entry.set_text(birth)
    def set_death_entry_text(self, death):
        self.death_entry.set_text(death)
    def set_name_entry_text(self, name):
        self.name_entry.set_text(name)
    def set_start_entry_text(self, start):
        self.start_entry.set_text(start)
    def set_end_entry_text(self, end):
        self.end_entry.set_text(end)

    def trigger_add_window(self, caller):
        persons = self.data_manager.get_persons()
        for person in persons:
            self.persons_combobox.append_text(person[0])
        self.persons_combobox.hide()
        self.add_window.show()

    def trigger_see_window(self, caller):
        persons = self.data_manager.get_persons_in_group(self.group_id)
        persons_names = []
        for person in persons:
            list = []
            list.append(self.data_manager.get_person_by_id(person[0])[1])
            persons_names.append(list)
        listmodel = Gtk.ListStore(str)
        for item in persons_names :
            listmodel.append(item)
        filter = listmodel.filter_new()
        self.persons_treeview.set_model(filter)
        self.see_window.show()

    def show_window(self):
        if self.type == "Unknown":
            self.comboboxtext.set_active(0)
            self.name_box.show()
            self.start_box.hide()
            self.end_box.hide()
            self.stage_name_box.hide()
            self.real_name_box.hide()
            self.birth_box.hide()
            self.death_box.hide()
            self.see_button.set_sensitive(False)
            self.add_button.set_sensitive(False)
        elif self.type == "Person":
            self.comboboxtext.set_active(1)
            self.see_button.set_sensitive(False)
            self.add_button.set_sensitive(False)
        elif self.type == "Group":
            self.comboboxtext.set_active(2)
            self.see_button.set_sensitive(True)
            self.add_button.set_sensitive(True)
            self.group_id = self.data_manager.get_group(self.name_entry.get_text())[0]
        self.performer_window.show()


    def start(self):
        columns = ["Name"]
        name_list =[[" "]]
        for name in name_list:
            self.liststore.append(name)
        for index, column in enumerate(columns):
            # cellrenderer to render the text
            cell = Gtk.CellRendererText()
            # the column is created
            col = Gtk.TreeViewColumn(column, cell, text=index)
            # and it is appended to the treeview
            self.persons_treeview.append_column(col)
