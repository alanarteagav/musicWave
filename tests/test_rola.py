if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from music_wave.rola import Rola, Rola_builder
    else:
        from ..music_wave.rola import Rola, Rola_builder

import unittest

class TestRola(unittest.TestCase):

    def setUp(self):
        self.rola_test = Rola()

    def setDown(self):
        pass

    def test_set_get_id(self):
        self.assertEqual(self.rola_test.get_id(), 0, 'get id fail')
        self.rola_test.set_id(113)
        self.assertEqual(self.rola_test.get_id(), 113, 'set id fail')

    def test_set_get_performer(self):
        self.assertEqual(self.rola_test.get_performer(), 0, 'get performer fail')
        self.rola_test.set_performer(113)
        self.assertEqual(self.rola_test.get_performer(), 113, 'set performer fail')

    def test_set_get_album(self):
        self.assertEqual(self.rola_test.get_album(), 0, 'get album fail')
        self.rola_test.set_album(113)
        self.assertEqual(self.rola_test.get_album(), 113, 'set album fail')

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

    def test_rola_builder(self):
        new_rola_test = Rola_builder() \
                        .with_id(2) \
                        .with_performer(2) \
                        .with_album(1) \
                        .with_path("shaffer/neiman/caravan_live.mp3") \
                        .with_title("Caravan (live)") \
                        .with_track(6) \
                        .with_year(2014) \
                        .with_genre("jazz")
        self.assertEqual(new_rola_test.get_id(), 2,
                         'build id fail')
        self.assertEqual(new_rola_test.get_performer(), 2,
                         'build performer fail')
        self.assertEqual(new_rola_test.get_album(), 1,
                         'build album fail')
        self.assertEqual(new_rola_test.get_path(),
                        "shaffer/neiman/caravan_live.mp3",
                         'build path fail')
        self.assertEqual(new_rola_test.get_title(), "Caravan (live)",
                         'build title fail')
        self.assertEqual(new_rola_test.get_track(), 6,
                         'build track fail')
        self.assertEqual(new_rola_test.get_year(), 2014,
                         'build year fail')
        self.assertEqual(new_rola_test.get_genre(), "jazz",
                         'get genre fail')

if __name__ == '__main__':
    unittest.main()
