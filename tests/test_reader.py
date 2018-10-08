if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from music_wave.miner import Miner
        from music_wave.reader import Reader
    else:
        from ..music_wave.miner import Miner
        from ..music_wave.reader import Reader

import os
import unittest
from mp3_tagger import MP3File, VERSION_2

class TestReader(unittest.TestCase):

    def setUp(self):
        miner_auxiliar = Miner(directory="", database_name="test.db")
        miner_auxiliar.create_database()

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

        miner_auxiliar.populate_database(path.dirname(path.dirname(path.abspath(__file__))))

        self.reader_test = Reader(directory = "", database_name = "test.db")

    def tearDown(self):
        os.remove("testA.mp3")
        os.remove("testB.mp3")
        os.remove("test.db")

    def test_get_rolas_from_database(self):
        rolas = self.reader_test.get_rolas_from_database()

if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestReader)
    except:
        pass
    unittest.TextTestRunner(verbosity=2).run(suite)
