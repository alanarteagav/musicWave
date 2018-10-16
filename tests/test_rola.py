from music_wave.rola import Rola

import unittest

class TestRola(unittest.TestCase):

    def setUp(self):
        self.rola_test = Rola(id = 0, performer_id = 0, album_id = 0,
                            path = 'null', title = 'null', track = 0,
                            year = 0, genre = 'null')

    def test_set_get_id(self):
        self.assertEqual(self.rola_test.get_id(), 0, 'get id fail')
        self.rola_test.set_id(113)
        self.assertEqual(self.rola_test.get_id(), 113, 'set id fail')

    def test_set_get_performer(self):
        self.assertEqual(self.rola_test.get_performer_id(), 0, 'get performer fail')
        self.rola_test.set_performer_id(113)
        self.assertEqual(self.rola_test.get_performer_id(), 113, 'set performer fail')

    def test_set_get_album(self):
        self.assertEqual(self.rola_test.get_album_id(), 0, 'get album fail')
        self.rola_test.set_album_id(113)
        self.assertEqual(self.rola_test.get_album_id(), 113, 'set album fail')

    def test_set_get_path(self):
        self.assertEqual(self.rola_test.get_path(), "null", 'get path fail')
        self.rola_test.set_path("shaffer/fletcher/Caravan.mp3")
        self.assertEqual(self.rola_test.get_path(), "shaffer/fletcher/Caravan.mp3",
                        'set path fail')

    def test_set_get_title(self):
        self.assertEqual(self.rola_test.get_title(), "null", 'get title fail')
        self.rola_test.set_title("Whiplash")
        self.assertEqual(self.rola_test.get_title(), "Whiplash", 'set title fail')

    def test_set_get_track(self):
        self.assertEqual(self.rola_test.get_track(), 0, 'get track fail')
        self.rola_test.set_track(66)
        self.assertEqual(self.rola_test.get_track(), 66, 'set track fail')

    def test_set_get_year(self):
        self.assertEqual(self.rola_test.get_year(), 0, 'get year fail')
        self.rola_test.set_year(1997)
        self.assertEqual(self.rola_test.get_year(), 1997, 'set year fail')

    def test_set_get_genre(self):
        self.assertEqual(self.rola_test.get_genre(), "null", 'get genre fail')
        self.rola_test.set_genre("jazz")
        self.assertEqual(self.rola_test.get_genre(), "jazz", 'set genre fail')

if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestRola)
    except:
        pass
    unittest.TextTestRunner(verbosity=2).run(suite)
