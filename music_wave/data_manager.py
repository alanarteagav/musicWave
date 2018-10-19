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
        for album, album_value in albums.items():
            cursor.execute('INSERT INTO albums ( id_album, name, year) \
                            VALUES (?, ?, ?)', (album_value[0], album, album_value[1]))
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

    def get_persons(self):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT persons.stage_name \
                        FROM persons ")
        persons = cursor.fetchall()
        connection.close()
        return persons

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
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rolas WHERE id_rola = ?", [id])
        rola = cursor.fetchone()
        connection.close()
        return rola

    def get_person(self, stage_name):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM persons WHERE stage_name = ?", [stage_name])
        person = cursor.fetchone()
        connection.close()
        return person

    def get_person_by_id(self, id_person):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM persons WHERE id_person = ?", [id_person])
        person = cursor.fetchone()
        connection.close()
        return person

    def get_persons_in_group(self, group_id):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM in_group WHERE id_group = ?", [group_id])
        persons = cursor.fetchall()
        connection.close()
        return persons

    def get_group(self, name):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM groups WHERE name = ?", [name])
        group = cursor.fetchone()
        connection.close()
        return group

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

    def execute_and_get_ids(self, command):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute(command)
        identifiers_from_database = cursor.fetchall()
        connection.close()
        identifiers = []
        if len(identifiers_from_database) != 0 :
            for id in identifiers_from_database:
                identifiers.append(id[0])
        return identifiers

    def update_album(self, id, name, year):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('UPDATE albums \
                        SET name = ?, year = ?\
                        WHERE id_album = ?' , (name, year, id))
        connection.commit()
        connection.close()

    def update_rola(self, id, title, track, year, genre):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('UPDATE rolas \
                        SET title = ?, track = ?, year = ?, genre = ? \
                        WHERE id_rola = ?' , (title, track, year, genre, id))
        connection.commit()
        connection.close()

    def update_performer(self, id, type, name):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('UPDATE performers \
                        SET  id_type = ?, name = ?\
                        WHERE id_performer = ?' , (type, name, id))
        connection.commit()
        connection.close()

    def update_person(self, stage_name, real_name, birth_date, death_date):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('UPDATE persons \
                        SET  stage_name = ?, real_name = ?, birth_date = ?, death_date = ?\
                        WHERE stage_name = ?' , (stage_name, real_name, birth_date, death_date, stage_name))
        connection.commit()
        connection.close()

    def update_group(self, name, start_date, end_date):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('UPDATE groups \
                        SET  name = ?, start_date = ?, end_date = ? \
                        WHERE name = ?' , (name, start_date, end_date, name))
        connection.commit()
        connection.close()

    def is_in_performers(self, name, type):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM performers WHERE name = ? AND id_type = ?", (name, type))
        performer = cursor.fetchone()
        connection.close()
        return not(performer == None)

    def is_unknown(self, id):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM performers WHERE id_performer = ? ", [id])
        performer = cursor.fetchone()
        connection.close()
        type = int(str(performer[1]))
        return type == 2

    def is_in_group(self, person_id, group_id):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM in_group WHERE id_person = ? AND id_group = ? ", [person_id, group_id])
        person = cursor.fetchone()
        connection.close()
        return not(person == None)

    def insert_performer(self, name, type):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO performers (id_type, name) \
                        VALUES (?, ?)', (type, name))
        connection.commit()
        connection.close()

    def insert_person(self, stage_name, real_name, birth_date, death_date):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO persons (stage_name, real_name, birth_date, death_date) \
                        VALUES (?, ?, ?, ?)', (stage_name, real_name, birth_date, death_date))
        connection.commit()
        connection.close()

    def insert_group(self, name, start_date, end_date):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO groups (name, start_date, end_date) \
                        VALUES (?, ?, ?)', (name, start_date, end_date))
        connection.commit()
        connection.close()

    def insert_in_group(self, id_person, id_group):
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO in_group (id_person, id_group) \
                        VALUES (?, ?)', (id_person, id_group))
        connection.commit()
        connection.close()

    def get_performers_index():
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM table ORDER BY id DESC LIMIT 1")
        performer = cursor.fetchone()
        return int(str(performer[0])) + 1
