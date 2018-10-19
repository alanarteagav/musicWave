import sqlite3
from sqlite3 import Error
from music_wave.rola import Rola

class DataManager :
    """Data access object, used to interact with the program database,
       and make queries and insertions in the database."""

    def __init__(self, directory, database_name):
        """Class constructor, receives a directory in which the database will
           be stored, and the name of the database file.

           Parameters:

           directory (str) : the directory of the database.

           database_name (str) : the name of the database."""
        self.directory = directory
        self.database_name = database_name

    def create_database(self):
        """Method that creates a database with the name and directory specified
           in the constructor, it does not receive any parameter."""
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
        """Method that receives rolas, performers and albums dictionaries
           (obtained with the corresponding methods of the miner class),
           and uses them to fill an existing database.

           Parameters :

           rolas ( dict {int : rola} ) : a dictionary of rolas.

           performers ( dict { str : int } ) : a dictionary of performers.

           albums ( dict { str : int } ) : a dictionary of albums."""

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
        """Method that returns a dictionary of performers obtained from the
           database.

           Returns : a dictionary of performers ( dict { str : int} )"""
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
        """Method that returns a list of tuples of persons obtained from the
           database.

           Returns : list of tuples of persons"""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT persons.stage_name \
                        FROM persons ")
        persons = cursor.fetchall()
        connection.close()
        return persons

    def get_albums(self):
        """Method that returns a dictionary of albums obtained from the
           database.

           Returns : a dictionary of albums ( dict { str : int} )"""
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
        """Method that returns a dictionary of rolas obtained from the
           database.

           Returns : a dictionary of rolas ( dict { int : rola} )"""
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
        """Method that returns a dictionary of rolas obtained from the
           database.

           Returns : a dictionary of rolas ( dict { int : rola} )"""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM performers WHERE id_performer = ?", [id])
        performer = cursor.fetchone()
        connection.close()
        return performer

    def get_album(self, id):
        """Method that returns a tuple containing an specific album, given
           its identifier.

           Parameter: id (int) : the album identifier.

           Returns : a tuple containing the album."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM albums WHERE id_album = ?", [id])
        album = cursor.fetchone()
        connection.close()
        return album

    def get_rola(self, id):
        """Method that returns a tuple containing an specific rola, given
           its identifier.

           Parameter: id (int) : the rola identifier.

           Returns : a tuple containing the rola."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rolas WHERE id_rola = ?", [id])
        rola = cursor.fetchone()
        connection.close()
        return rola

    def get_person(self, stage_name):
        """Method that returns a tuple containing an specific person, given
           its stage name.

           Parameter: stage_name (str) : the person stage name.

           Returns : a tuple containing the person."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM persons WHERE stage_name = ?", [stage_name])
        person = cursor.fetchone()
        connection.close()
        return person

    def get_person_by_id(self, id_person):
        """Method that returns a tuple containing an specific person, given
           its identifier.

           Parameter: id_person (int) : the person identifier.

           Returns : a tuple containing the person."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM persons WHERE id_person = ?", [id_person])
        person = cursor.fetchone()
        connection.close()
        return person

    def get_persons_in_group(self, group_id):
        """Method that returns all the persons in a group, given the group
           identifier.

           Parameter: group_id (int) : the group identifier.

           Returns : list of tuples of the persons in the specific group"""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM in_group WHERE id_group = ?", [group_id])
        persons = cursor.fetchall()
        connection.close()
        return persons

    def get_group(self, name):
        """Method that returns a tuple containing an specific group, given
           its name.

           Parameter: id_person (int) : the group name.

           Returns : a tuple containing the group."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM groups WHERE name = ?", [name])
        group = cursor.fetchone()
        connection.close()
        return group

    def insert_performers(self, performers):
        """Method that inserts a group of performers into the database.

           Parameter: performers ( dict { str : int} ) : a dictionary
           containing the performers."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        for performer, performer_id in performers.items():
            cursor.execute('INSERT INTO performers (id_performer, id_type, name) \
                            VALUES (?, ?, ?)', (performer_id, 2, performer))
        connection.commit()
        connection.close()

    def insert_albums(self, albums):
        """Method that inserts a group of albums into the database.

           Parameter: albums ( dict { str : int} ) : a dictionary
           containing the albums."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        for album, album_id in albums.items():
            cursor.execute('INSERT INTO albums (id_album, name) \
                            VALUES (?, ?)', (album_id, album))
        connection.commit()
        connection.close()

    def insert_rolas(self, rolas):
        """Method that inserts a group of rolas into the database.

           Parameter: rolas ( dict { int : rola} ) : a dictionary
           containing the rolas."""
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
        """Method that executes a query, defined by a sql string, and returns
           the identifiers in the rolas table such that satisfy the query
           parameters.

           Parameter: command (str) : a sql query string.

           Returns : a list of all the identifiers that satisfy the query
                     parameters."""
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
        """Updates the values of an specific album in the database.

           Parameters:

           id (int) : the identifier of the album.

           name (str) : the new album name.

           year (int) : the new album year."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('UPDATE albums \
                        SET name = ?, year = ?\
                        WHERE id_album = ?' , (name, year, id))
        connection.commit()
        connection.close()

    def update_rola(self, id, title, track, year, genre):
        """Updates the values of an specific rola in the database.

           Parameters:

           id (int) : the identifier of the rola.

           title (str) : the new rola title.

           track (int) : the new rola track number.

           year (int) : the new rola year.

           genre (str) : the new rola genre."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('UPDATE rolas \
                        SET title = ?, track = ?, year = ?, genre = ? \
                        WHERE id_rola = ?' , (title, track, year, genre, id))
        connection.commit()
        connection.close()

    def update_performer(self, id, type, name):
        """Updates the values of an specific performer in the database.

           Parameters:

           id (int) : the identifier of the performer.

           type (int) : the new performer type.

           name (str) : the new performer name."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('UPDATE performers \
                        SET  id_type = ?, name = ?\
                        WHERE id_performer = ?' , (type, name, id))
        connection.commit()
        connection.close()

    def update_person(self, stage_name, real_name, birth_date, death_date):
        """Updates the values of an specific person in the database.

           Parameters:

           stage_name (str) : the stage_name of the person. (used to identify
           the person).

           real_name (str) : the new person real name.

           birth_date (str) : the new person birth_date.

           death_date (str) : the new person death_date."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('UPDATE persons \
                        SET  stage_name = ?, real_name = ?, birth_date = ?, death_date = ?\
                        WHERE stage_name = ?' , (stage_name, real_name, birth_date, death_date, stage_name))
        connection.commit()
        connection.close()

    def update_group(self, name, start_date, end_date):
        """Updates the values of an specific group in the database.

           Parameters:

           name (str) : the name of the group. (used to identify
           the group).

           start_date (str) : the new group start date.

           end_date (str) : the new group end date."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('UPDATE groups \
                        SET  name = ?, start_date = ?, end_date = ? \
                        WHERE name = ?' , (name, start_date, end_date, name))
        connection.commit()
        connection.close()

    def is_in_performers(self, name, type):
        """Checks if an specific performer already exists in the database.

           Parameters:

           name (str) : the name of the performer.

           type (int) : the performer type."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM performers WHERE name = ? AND id_type = ?", (name, type))
        performer = cursor.fetchone()
        connection.close()
        return not(performer == None)

    def is_unknown(self, id):
        """Checks if the type of an specific performer is unknown.

           Parameters:

           id (int) : the performer id."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM performers WHERE id_performer = ? ", [id])
        performer = cursor.fetchone()
        connection.close()
        type = int(str(performer[1]))
        return type == 2

    def is_in_group(self, person_id, group_id):
        """Checks if an specific person is in an specific group.

           Parameters:

           person_id (int) : the person identifier.

           group_id (int) : the group identifier."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM in_group WHERE id_person = ? AND id_group = ? ", [person_id, group_id])
        person = cursor.fetchone()
        connection.close()
        return not(person == None)

    def insert_performer(self, name, type):
        """Inserts a new performer into the performers table.

           Parameters:

           name (str) : the performer name.

           type (int) : the performer type."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO performers (id_type, name) \
                        VALUES (?, ?)', (type, name))
        connection.commit()
        connection.close()

    def insert_person(self, stage_name, real_name, birth_date, death_date):
        """Inserts a new person into the persons table.

           Parameters:

           stage_name (str) : the stage_name of the person.

           real_name (str) : the new person real name.

           birth_date (str) : the new person birth_date.

           death_date (str) : the new person death_date."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO persons (stage_name, real_name, birth_date, death_date) \
                        VALUES (?, ?, ?, ?)', (stage_name, real_name, birth_date, death_date))
        connection.commit()
        connection.close()

    def insert_group(self, name, start_date, end_date):
        """Inserts a new group into the groups table.

           Parameters:

           name (str) : the name of the group.

           start_date (str) : the new group start date.

           end_date (str) : the new group end date."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO groups (name, start_date, end_date) \
                        VALUES (?, ?, ?)', (name, start_date, end_date))
        connection.commit()
        connection.close()

    def insert_in_group(self, id_person, id_group):
        """Inserts a person into a group using the in_group table.

           Parameters:

           person_id (int) : the person identifier.

           group_id (int) : the group identifier."""
        connection = sqlite3.connect(self.directory + self.database_name)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO in_group (id_person, id_group) \
                        VALUES (?, ?)', (id_person, id_group))
        connection.commit()
        connection.close()
