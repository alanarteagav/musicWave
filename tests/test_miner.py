if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from music_wave.miner import Miner
    else:
        from ..music_wave.miner import Miner

import unittest

class TestMiner(unittest.TestCase):

    def setUp(self):
        self.miner_test = Miner(path)

    def setDown(self):
        pass

    def test_create_database(self):
        self.self.assert_(False)

    def test_populate_database(self):
        self.self.assert_(False)


if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMiner)
    except:
        pass
    unittest.TextTestRunner(verbosity=2).run(suite)
