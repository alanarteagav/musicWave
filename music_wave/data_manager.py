import sqlite3
from sqlite3 import Error
from .rola import Rola

class Data_manager :

    def __init__(self, directory, database_name):
        self.directory = directory
        self.database_name = database_name

    def create_database(self):
        pass

    def populate_database(self, rolas, performers, albums):
        pass

    def get_performers(self):
        pass

    def get_albums(self):
        pass

    def get_rolas(self):
        pass

    def get_performer(self, id):
        pass

    def get_album(self, id):
        pass

    def get_rola(self, id):
        pass

    def insert_performers(self, performers):
        pass

    def insert_albums(self, albums):
        pass

    def insert_rolas(self, rolas):
        pass

    def insert_performer(self, performer):
        pass

    def insert_album(self, album):
        pass

    def insert_rola(self, rola):
        pass
