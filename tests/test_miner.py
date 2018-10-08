if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from music_wave.miner import Miner
    else:
        from ..music_wave.miner import Miner

import unittest
import sqlite3
import os
from sqlite3 import Error
from mp3_tagger import MP3File, VERSION_2

class TestMinerCreateDatabase(unittest.TestCase):

    def setUp(self):
        self.miner_test = Miner(directory="", database_name="test.db")

    def tearDown(self):
        os.remove("test.db")

    def test_create_database(self):
        self.miner_test.create_database()
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

class TestMinerPopulateDatabase(unittest.TestCase):

    def setUp(self):
        self.miner_test = Miner(directory="", database_name="test.db")

    def tearDown(self):
        os.remove("test.db")
        os.remove("testA.mp3")
        os.remove("testB.mp3")


    def test_populate_database(self):
        mp3_file = open("testA.mp3","w+")
        mp3_file.close()
        mp3_file = open("testB.mp3","w+")
        mp3_file.close()

        mp3_testA = MP3File("testA.mp3")
        mp3_testA.set_version(VERSION_2)
        mp3_testA.comment = "Comment"
        mp3_testA.song = "Caravan"
        mp3_testA.artist = "Andrew Neiman"
        mp3_testA.album = "Shaffer Conservatory Studio Band"
        mp3_testA.track = "6"
        mp3_testA.year = "2014"
        mp3_testA.genre = "Jazz"
        mp3_testA.save()

        mp3_testA = MP3File("testB.mp3")
        mp3_testA.set_version(VERSION_2)
        mp3_testA.comment = "Comment"
        mp3_testA.song = "Lost Stars"
        mp3_testA.artist = "Dave Kohl"
        mp3_testA.album = "On The Road"
        mp3_testA.track = "1"
        mp3_testA.year = "2012"
        mp3_testA.genre = "Pop"
        mp3_testA.save()

        self.miner_test.create_database()
        self.miner_test.populate_database(path.dirname(path.dirname(path.abspath(__file__))))

        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT rolas.title, performers.name, \
                                   albums.name, rolas.genre \
                            FROM rolas \
                            INNER JOIN albums ON albums.id_album = rolas.id_album \
                            INNER JOIN performers ON performers.id_performer \
                                = rolas.id_performer")
        except:
            self.fail('Could not get songs from database')

        song1 = ('Lost Stars', 'Dave Kohl',
                 'On The Road', 'Pop')
        song2 = ('Caravan', 'Andrew Neiman',
                 'Shaffer Conservatory Studio Band', 'Jazz')
        try:
            songs_from_database = cursor.fetchall()
            self.assertTrue(song1 == songs_from_database[0] or \
                            song1 == songs_from_database[1],
                            'message')
            self.assertTrue(song2 == songs_from_database[0] or \
                            song2 == songs_from_database[1],
                            'message')
        except:
            self.fail('Could not get songs from database')

if __name__ == '__main__':

    test_classes_to_run = [TestMinerCreateDatabase,
                           TestMinerPopulateDatabase]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    final_suite = unittest.TestSuite(suites_list)

    unittest.TextTestRunner(verbosity=2).run(final_suite)
