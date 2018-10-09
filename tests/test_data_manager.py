if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from music_wave.data_manager import Data_manager
        from music_wave.rola import Rola
    else:
        from ..music_wave.data_manager import Data_manager
        from ..music_wave.rola import Rola

import os
import unittest
import sqlite3
from sqlite3 import Error

class TestCreateDatabase(unittest.TestCase):

    def setUp(self):
        self.data_manager = Data_manager(directory="", database_name="test.db")

    def tearDown(self):
        os.remove("test.db")

    def test_create_database(self):
        self.data_manager.create_database()
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master \
                        WHERE type='table' AND name='performers'")
        try:
            self.assertEqual(cursor.fetchone()[0], "performers",
                             'performers table not created')
        except:
            self.fail('Fail, could not get table name')

        cursor.execute("SELECT name FROM sqlite_master \
                        WHERE type='table' AND name='persons'")
        try:
            self.assertEqual(cursor.fetchone()[0], "persons",
                             'persons table not created')
        except:
            self.fail('Fail, could not get table name')

        cursor.execute("SELECT name FROM sqlite_master \
                        WHERE type='table' AND name='groups'")
        try:
            self.assertEqual(cursor.fetchone()[0], "groups",
                             'groups table not created')
        except:
            self.fail('Fail, could not get table name')

        cursor.execute("SELECT name FROM sqlite_master \
                        WHERE type='table' AND name='albums'")
        try:
            self.assertEqual(cursor.fetchone()[0], "albums",
                             'albums table not created')
        except:
            self.fail('Fail, could not get table name')

        cursor.execute("SELECT name FROM sqlite_master \
                        WHERE type='table' AND name='rolas'")
        try:
            self.assertEqual(cursor.fetchone()[0], "rolas",
                             'rolas table not created')
        except:
            self.fail('Fail, could not get table name')

        cursor.execute("SELECT name FROM sqlite_master \
                        WHERE type='table' AND name='in_group'")
        try:
            self.assertEqual(cursor.fetchone()[0], "in_group",
                             'in_group table not created')
        except:
            self.fail('Fail, could not get table name')

class TestPopulateDatabase(unittest.TestCase):

    def setUp(self):
        self.path = str(path.dirname(path.dirname(path.abspath(__file__))))
        self.data_manager = Data_manager(directory="", database_name="test.db")

    def tearDown(self):
        os.remove("test.db")

    def test_populate_database(self):
        self.data_manager.create_database()

        rolaA = Rola(id = 1, performer_id = 1, album_id = 1,
                     path = 'path/to/rolaA.mp3', title = 'Caravan', track = 6,
                     year = 2014, genre = 'Jazz')
        rolaB = Rola(id = 2, performer_id = 2, album_id = 2,
                     path = 'path/to/rolaB.mp3', title = 'Lost Stars', track = 1,
                     year = 2012, genre = 'Pop')
        rolas = {}
        rolas[1] = rolaA
        rolas[2] = rolaB

        performers = {}
        performers['Andrew Neiman'] = 1
        performers['Dave Kohl'] = 2

        albums = {}
        albums['Shaffer Conservatory Studio Band'] = 1
        albums['On The Road'] = 2

        self.data_manager.populate_database(rolas, performers, albums)

        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT rolas.id_rola, rolas.title, performers.name, \
                                   albums.name, rolas.track, rolas.year, \
                                   rolas.genre \
                            FROM rolas \
                            INNER JOIN albums ON albums.id_album = rolas.id_album \
                            INNER JOIN performers ON performers.id_performer \
                                = rolas.id_performer")
        except:
            self.fail('Could not get songs from database')
        try:
            songs_from_database = cursor.fetchall()
            if len(songs_from_database) != 2 :
                self.fail('Not enough songs in database')
            for song in songs_from_database:
                if song[0] == 1:
                    self.assertEqual(rolaA.get_title(), song[1],
                                     'Fail, not the same title.')
                    self.assertEqual('Andrew Neiman', song[2],
                                     'Fail, not the same performer.')
                    self.assertEqual('Shaffer Conservatory Studio Band', song[3],
                                     'Fail, not the same album.')
                    self.assertEqual(rolaA.get_track(), song[4],
                                     'Fail, not the same track.')
                    self.assertEqual(rolaA.get_year(), song[5],
                                     'Fail, not the same year.')
                    self.assertEqual(rolaA.get_genre(), song[6],
                                     'Fail, not the same genre.')
                elif song[0] == 2:
                    self.assertEqual(rolaB.get_title(), song[1],
                                     'Fail, not the same title.')
                    self.assertEqual('Dave Kohl', song[2],
                                     'Fail, not the same performer.')
                    self.assertEqual('On The Road', song[3],
                                     'Fail, not the same album.')
                    self.assertEqual(rolaB.get_track(), song[4],
                                     'Fail, not the same track.')
                    self.assertEqual(rolaB.get_year(), song[5],
                                     'Fail, not the same year.')
                    self.assertEqual(rolaB.get_genre(), song[6],
                                     'Fail, not the same genre.')
                else:
                    self.fail('Could not get songs from database')
        except:
            self.fail('Could not get songs from database')

    def test_insert_get_performers(self):
        self.data_manager.create_database()
        performers = {}
        performers['Andrew Neiman'] = 1
        performers['Dave Kohl'] = 2

        self.data_manager.insert_performers(performers)
        performers_database = self.data_manager.get_performers()
        self.assertEqual(performers, performers_database,
                         'Not the same performers')

    def test_insert_get_albums(self):
        self.data_manager.create_database()
        albums = {}
        albums['Shaffer Conservatory Studio Band'] = 1
        albums['On The Road'] = 2

        self.data_manager.insert_albums(albums)
        albums_database = self.data_manager.get_albums()
        self.assertEqual(albums, albums_database,
                         'Not the same albums')

    def test_insert_get_rolas(self):
        self.data_manager.create_database()
        rolaA = Rola(id = 1, performer_id = 1, album_id = 1,
                     path = 'path/to/rolaA.mp3', title = 'Caravan', track = 6,
                     year = 2014, genre = 'Jazz')
        rolaB = Rola(id = 2, performer_id = 2, album_id = 2,
                     path = 'path/to/rolaB.mp3', title = 'Lost Stars', track = 1,
                     year = 2012, genre = 'Pop')
        rolas = {}
        rolas[1] = rolaA
        rolas[2] = rolaB

        self.data_manager.insert_rolas(rolas)
        rolas_database = self.data_manager.get_rolas()

    def test_get_performer(self):
        self.data_manager.create_database()
        performers = {}
        performers['Andrew Neiman'] = 1
        performers['Dave Kohl'] = 2
        self.data_manager.insert_performers(performers)

        performerA = self.data_manager.get_performer(1)
        try:
            self.assertEqual('Andrew Neiman', performerA[2],
                             'Not the same performer')
        except:
            self.fail('Could not get performer')
        performerB = self.data_manager.get_performer(2)
        try:
            self.assertEqual('Dave Kohl', performerB[2],
                             'Not the same performer')
        except:
            self.fail('Could not get performer')

    def test_get_album(self):
        self.data_manager.create_database()
        albums = {}
        albums['Shaffer Conservatory Studio Band'] = 1
        albums['On The Road'] = 2
        self.data_manager.insert_albums(albums)

        albumA = self.data_manager.get_album(1)
        try:
            self.assertEqual('Shaffer Conservatory Studio Band', albumA[2],
                             'Not the same album')
        except:
            self.fail('Could not get album')
        albumB = self.data_manager.get_album(2)
        try:
            self.assertEqual('On The Road', albumB[2],
                             'Not the same album')
        except:
            self.fail('Could not get album')

if __name__ == '__main__':

    test_classes_to_run = [TestCreateDatabase,
                           TestPopulateDatabase]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    final_suite = unittest.TestSuite(suites_list)

    unittest.TextTestRunner(verbosity=2).run(final_suite)
