if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from music_wave.miner import Miner
    else:
        from ..music_wave.miner import Miner

import unittest
import os
from mp3_tagger import MP3File, VERSION_2

class TestMiner(unittest.TestCase):

    def setUp(self):
        self.path = str(path.dirname(path.dirname(path.abspath(__file__))))
        self.miner_test = Miner(path = self.path)

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
        mp3_testA.track = "1/12"
        mp3_testA.year = "2012"
        mp3_testA.genre = "Pop"
        mp3_testA.save()

    def tearDown(self):
        os.remove("testA.mp3")
        os.remove("testB.mp3")

    def test_get_rolas(self):
        self.miner_test.mine()
        rolas = self.miner_test.get_rolas()
        performers = self.miner_test.get_performers()
        albums = self.miner_test.get_albums()
        if len(rolas) != 2 :
            self.fail('Not returned correct dict')
        for rola in rolas.values():
            if rola.get_path() == self.path + "/testA.mp3":
                self.assertEqual(rola.get_performer_id(),
                                 performers['Andrew Neiman'],
                                 'Performer tag FAIL')
                self.assertEqual(rola.get_album_id(),
                                 albums['Shaffer Conservatory Studio Band'],
                                 'Album tag FAIL')
                self.assertEqual(rola.get_path(), self.path + "/testA.mp3",
                                 'Path tag FAIL')
                self.assertEqual(rola.get_title(), "Caravan", 'Title tag FAIL')
                self.assertEqual(rola.get_track(), 6, 'Track tag FAIL')
                self.assertEqual(rola.get_year(), 2014, 'Year tag FAIL')
                self.assertEqual(rola.get_genre(), 'Jazz', 'Genre tag FAIL')
            elif rola.get_path() == self.path + "/testB.mp3":
                self.assertEqual(rola.get_performer_id(),
                                 performers['Dave Kohl'],
                                 'Performer tag FAIL')
                self.assertEqual(rola.get_album_id(),
                                 albums['On The Road'],
                                 'Album tag FAIL')
                self.assertEqual(rola.get_path(),
                                 self.path + "/testB.mp3",
                                 'Path tag FAIL')
                self.assertEqual(rola.get_title(), "Lost Stars", 'Title tag FAIL')
                self.assertEqual(rola.get_track(), 1, 'Track tag FAIL')
                self.assertEqual(rola.get_year(), 2012, 'Year tag FAIL')
                self.assertEqual(rola.get_genre(), 'Pop', 'Genre tag FAIL')
            else :
                self.fail('Could not read from mp3 files')

    def test_get_performers(self):
        self.miner_test.mine()
        performers = self.miner_test.get_performers()
        if len(performers) != 2 :
            self.fail('Not returned correct dict')
        for performer in performers:
            self.assertTrue(performer == 'Andrew Neiman' or \
                            performer == 'Dave Kohl',
                            'Could not get artist tag')

    def test_get_albums(self):
        self.miner_test.mine()
        albums = self.miner_test.get_albums()
        if len(albums) != 2 :
            self.fail('Not returned correct dict')
        for album in albums:
            self.assertTrue(album == 'Shaffer Conservatory Studio Band' or \
                            album == 'On The Road',
                            'Could not get album tag')


if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMiner)
    except:
        pass
    unittest.TextTestRunner(verbosity=2).run(suite)
