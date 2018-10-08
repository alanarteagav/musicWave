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

class TestMiner(unittest.TestCase):

    def setUp(self):
        self.miner_test = Miner(directory="", database_name="test.db")

    def setDown(self):
        pass

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
        os.remove("test.db")


    def test_populate_database(self):
        self.fail('Fail')


if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMiner)
    except:
        pass
    unittest.TextTestRunner(verbosity=2).run(suite)
