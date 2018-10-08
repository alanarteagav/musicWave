if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from music_wave.reader import Reader
    else:
        from ..music_wave.reader import Reader

import unittest

class TestReader(unittest.TestCase):

    def setUp(self):
        self.miner_test = Reader(path)

    def setDown(self):
        pass

    def test_get_rolas_from_database(self):
        self.assert_(False)


if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestReader)
    except:
        pass
    unittest.TextTestRunner(verbosity=2).run(suite)
