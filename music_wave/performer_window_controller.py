from .data_manager import DataManager

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PerformerWindowController:
    def __init__(self):
        self.data_manager = DataManager("", "rolas.db")

        self.type = "Unknown"

        self.id = 0
        self.old_name = ""
        self.builder = Gtk.Builder()
        self.builder.add_from_file("resources/performer.glade")
        self.performer_window = self.builder.get_object("performer_window")

        self.stage_entry = self.builder.get_object("stage_entry")
        self.real_entry = self.builder.get_object("real_entry")
        self.birth_entry = self.builder.get_object("birth_entry")
        self.death_entry = self.builder.get_object("death_entry")
        self.name_entry = self.builder.get_object("name_entry")
        self.start_entry = self.builder.get_object("start_entry")
        self.end_entry = self.builder.get_object("end_entry")

        self.comboboxtext = self.builder.get_object("comboboxtext")
        self.builder.connect_signals({"type_changed" : self.change_type})

        self.stage_name_box = self.builder.get_object("stage_name_box")
        self.real_name_box = self.builder.get_object("real_name_box")
        self.birth_box = self.builder.get_object("birth_box")
        self.death_box = self.builder.get_object("death_box")

        self.name_box = self.builder.get_object("name_box")
        self.start_box = self.builder.get_object("start_box")
        self.end_box = self.builder.get_object("end_box")


        self.discard_button = self.builder.get_object("discard_button")
        self.discard_button.connect("clicked", self.hide_window_with_button)

        self.apply_button = self.builder.get_object("apply_button")
        self.apply_button.connect("clicked", self.apply_changes)

        self.performer_window.connect("delete-event", self.hide_window)
        self.performer_window.connect("destroy", self.hide_window)

        self.filter = None

    def hide_window(self, window, event):
        window.hide()
        return True

    def hide_window_with_button(self, caller):
        self.performer_window.hide()
        return True

    def change_type(self, caller):
        self.type = self.comboboxtext.get_active_text()
        if self.type == "Group":
            self.name_box.show()
            self.start_box.show()
            self.end_box.show()
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
        elif self.type == "Unknown":
            self.name_box.show()
            self.start_box.hide()
            self.end_box.hide()
            self.stage_name_box.hide()
            self.real_name_box.hide()
            self.birth_box.hide()
            self.death_box.hide()
        return True

    def clear_entries(self):
        self.stage_entry.set_text("")
        self.real_entry.set_text("")
        self.birth_entry.set_text("")
        self.death_entry.set_text("")
        self.name_entry.set_text("")
        self.start_entry.set_text("")
        self.end_entry.set_text("")

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
        elif self.type == "Person":
            self.comboboxtext.set_active(1)
        elif self.type == "Group":
            self.comboboxtext.set_active(2)
        self.performer_window.show()
