import sqlite3
from sqlite3 import Error
from .rola import Rola


class DataManager :

    def __init__(self, directory, database_name):
        self.directory = directory
        self.database_name = database_name

    def create_database(self):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE types (
                              id_type INTEGER PRIMARY KEY ,
                              description TEXT
                           )""")
        cursor.execute("""INSERT INTO types VALUES (0 , 'Person ')""")
        cursor.execute("""INSERT INTO types VALUES (1 , 'Group ')""")
        cursor.execute("""INSERT INTO types VALUES (2 , 'Unknown ')""")
        cursor.execute("""CREATE TABLE performers (
                              id_performer INTEGER PRIMARY KEY ,
                              id_type INTEGER ,
                              name TEXT ,
                              FOREIGN KEY ( id_type ) REFERENCES types ( id_type )
                           )""")
        cursor.execute("""CREATE TABLE persons (
                              id_person INTEGER PRIMARY KEY ,
                              stage_name TEXT ,
                              real_name TEXT ,
                              birth_date TEXT ,
                              death_date TEXT
                           )""")
        cursor.execute("""CREATE TABLE groups (
                              id_group INTEGER PRIMARY KEY ,
                              name TEXT ,
                              start_date TEXT ,
                              end_date TEXT
                           )""")
        cursor.execute("""CREATE TABLE albums (
                              id_album INTEGER PRIMARY KEY ,
                              path TEXT ,
                              name TEXT ,
                              year INTEGER
                           )""")
        cursor.execute("""CREATE TABLE rolas (
                              id_rola INTEGER PRIMARY KEY ,
                              id_performer INTEGER ,
                              id_album INTEGER ,
                              path TEXT ,
                              title TEXT ,
                              track INTEGER ,
                              year INTEGER ,
                              genre TEXT ,
                              FOREIGN KEY ( id_performer )
                              REFERENCES performers ( id_performer ) ,
                              FOREIGN KEY ( id_album )
                              REFERENCES albums ( id_album )
                           )""")
        cursor.execute("""CREATE TABLE in_group (
                              id_person INTEGER ,
                              id_group INTEGER ,
                              PRIMARY KEY ( id_person , id_group ) ,
                              FOREIGN KEY ( id_person ) \
                              REFERENCES persons ( id_person ) ,
                              FOREIGN KEY ( id_group ) \
                              REFERENCES groups ( id_group )
                           )""")
        connection.commit()
        connection.close()

    def populate_database(self, rolas, performers, albums):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()

        for performer, performer_id in performers.items():
            cursor.execute('INSERT INTO performers (id_performer, id_type, name) \
                            VALUES (?, ?, ?)', (performer_id, 2, performer))
        for album, album_id in albums.items():
            cursor.execute('INSERT INTO albums ( id_album, name) \
                            VALUES (?, ?)', (album_id, album))
        for id, rola in rolas.items():
            cursor.execute('INSERT INTO rolas ( id_rola, id_performer, \
                                                id_album, path, title, \
                                                track, year, genre ) \
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                            (rola.get_id(), rola.get_performer_id(),
                             rola.get_album_id(), rola.get_path(), \
                             rola.get_title(), rola.get_track(),
                             rola.get_year(), rola.get_genre()))
        connection.commit()
        connection.close()

    def get_performers(self):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT performers.name, performers.id_performer \
                        FROM performers ")
        performers_from_database = cursor.fetchall()
        connection.close()
        performers = {}
        if len(performers_from_database) != 0 :
            for performer in performers_from_database:
                performers[performer[0]] = performer[1]
        return performers

    def get_albums(self):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT albums.name, albums.id_album \
                        FROM albums ")
        albums_from_database = cursor.fetchall()
        connection.close()
        albums = {}
        if len(albums_from_database) != 0 :
            for album in albums_from_database:
                albums[album[0]] = album[1]
        return albums

    def get_rolas(self):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rolas")
        rolas_from_database = cursor.fetchall()
        connection.close()
        rolas = {}
        if len(rolas_from_database) != 0 :
            for rola in rolas_from_database:
                new_rola = Rola(id = rola[0], performer_id = rola[1],
                                album_id = rola[2], path = rola[3],
                                title = rola[4], track = rola[5],
                                year = rola[6], genre = rola[7])
                rolas[rola[0]] = new_rola
        return rolas

    def get_performer(self, id):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM performers WHERE id_performer = ?", [id])
        performer = cursor.fetchone()
        connection.close()
        return performer

    def get_album(self, id):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM albums WHERE id_album = ?", [id])
        album = cursor.fetchone()
        connection.close()
        return album

    def get_rola(self, id):
        pass

    def insert_performers(self, performers):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        for performer, performer_id in performers.items():
            cursor.execute('INSERT INTO performers (id_performer, id_type, name) \
                            VALUES (?, ?, ?)', (performer_id, 2, performer))
        connection.commit()
        connection.close()

    def insert_albums(self, albums):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        for album, album_id in albums.items():
            cursor.execute('INSERT INTO albums (id_album, name) \
                            VALUES (?, ?)', (album_id, album))
        connection.commit()
        connection.close()

    def insert_rolas(self, rolas):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        for id, rola in rolas.items():
            cursor.execute('INSERT INTO rolas ( id_rola, id_performer, \
                                                id_album, path, title, \
                                                track, year, genre ) \
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                            (rola.get_id(), rola.get_performer_id(),
                             rola.get_album_id(), rola.get_path(), \
                             rola.get_title(), rola.get_track(),
                             rola.get_year(), rola.get_genre()))
        connection.commit()
        connection.close()

    def insert_performer(self, performer):
        pass

    def insert_album(self, album):
        pass

    def insert_rola(self, rola):
        pass
