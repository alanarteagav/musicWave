from music_wave.miner import Miner
import unittest
import os
from os import path
from mutagen.easyid3 import EasyID3

class TestMiner(unittest.TestCase):

    def setUp(self):
        self.path = str(path.dirname(path.dirname(path.abspath(__file__))))
        self.miner = Miner(path = self.path)

    def test_setup(self):
        self.miner.setup()
        self.miner.walk()
        for path in self.miner.get_paths():
            self.miner.mine(path)
        self.miner.setup()
        self.assertEqual({}, self.miner.get_rolas(), 'Rolas startup fail')
        self.assertEqual({'Unknown': 0}, self.miner.get_performers(),
                        'Performers startup fail')
        self.assertEqual({'Unknown': 0}, self.miner.get_albums(),
                        'Albums startup fail')
        self.assertEqual(0, self.miner.get_progress(), 'Progress startup fail')
        self.assertEqual(0, self.miner.get_total_files(),
                        'Total files startup fail')
        self.assertEqual([], self.miner.get_paths(), 'Paths startup fail')

    def test_get_rolas(self):
        self.miner.setup()
        self.miner.walk()
        for path in self.miner.get_paths():
            self.miner.mine(path)
        rolas = self.miner.get_rolas()
        performers = self.miner.get_performers()
        albums = self.miner.get_albums()
        if len(rolas) != 2 :
            self.fail('Not returned correct dict')

        for rola in rolas.values():
            if rola.get_path() == self.path + "/tests/test_resources/test1.mp3":
                self.assertEqual(rola.get_performer_id(), performers['Test Artist'],
                                 'Performer tag FAIL')
                self.assertEqual(rola.get_album_id(), albums['Test Album'],
                                 'Album tag FAIL')
                self.assertEqual(rola.get_path(),
                                 self.path + "/tests/test_resources/test1.mp3",
                                 'Path tag FAIL')
                self.assertEqual(rola.get_title(), "Test Title 1", 'Title tag FAIL')
                self.assertEqual(rola.get_track(), 1, 'Track tag FAIL')
                self.assertEqual(rola.get_year(), 2018, 'Year tag FAIL')
                self.assertEqual(rola.get_genre(), 'Rock', 'Genre tag FAIL')

            elif rola.get_path() == self.path + "/tests/test_resources/test2.mp3":
                self.assertEqual(rola.get_performer_id(), performers['Test Artist'],
                                 'Performer tag FAIL')
                self.assertEqual(rola.get_album_id(), albums['Test Album'],
                                 'Album tag FAIL')
                self.assertEqual(rola.get_path(),
                                 self.path + "/tests/test_resources/test2.mp3",
                                 'Path tag FAIL')
                self.assertEqual(rola.get_title(), "Test Title 2", 'Title tag FAIL')
                self.assertEqual(rola.get_track(), 2, 'Track tag FAIL')
                self.assertEqual(rola.get_year(), 2018, 'Year tag FAIL')
                self.assertEqual(rola.get_genre(), 'Rock', 'Genre tag FAIL')

            else:
                self.fail('Could not get rolas')

    def test_get_performers(self):
        self.miner.setup()
        self.miner.walk()
        for path in self.miner.get_paths():
            self.miner.mine(path)
        performers = self.miner.get_performers()
        if len(performers) != 2 :
            self.fail('Not returned correct dict')
        for performer in performers:
            self.assertTrue(performer == 'Unknown' or \
                            performer == 'Test Artist',
                            'Could not get artist tag')

    def test_get_albums(self):
        self.miner.setup()
        self.miner.walk()
        for path in self.miner.get_paths():
            self.miner.mine(path)
        albums = self.miner.get_albums()
        if len(albums) != 2 :
            self.fail('Not returned correct dict')
        for album in albums:
            self.assertTrue(album == 'Unknown' or \
                            album == 'Test Album',
                            'Could not get album tag')

if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMiner)
    except:
        pass
    unittest.TextTestRunner(verbosity=2).run(suite)
