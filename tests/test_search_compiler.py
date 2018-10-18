from music_wave.search_compiler import SearchCompiler

import unittest

class TestCompiler(unittest.TestCase):

    def setUp(self):
        self.compiler = SearchCompiler()

    def test_compile_title_search(self):
        title_search = "title : Caravan"
        expected_sql_search = "SELECT id_rola FROM rolas, albums, performers " \
                            + "WHERE rolas.id_album = albums.id_album " \
                            + "AND rolas.id_performer = performers.id_performer " \
                            + "AND (title LIKE '%Caravan%')"
        sql_search = self.compiler.compile(title_search)
        self.assertEqual(sql_search, expected_sql_search,
                        'Not expected sql string')

        multiple_title_search = "title  :  Caravan .  title    :   Lost Stars  "
        expected_sql_search = "SELECT id_rola FROM rolas, albums, performers " \
                            + "WHERE rolas.id_album = albums.id_album " \
                            + "AND rolas.id_performer = performers.id_performer " \
                            + "AND (title LIKE '%Caravan%' " \
                            + "OR title LIKE '%Lost Stars%')"
        sql_search = self.compiler.compile(multiple_title_search)
        self.assertEqual(sql_search, expected_sql_search,
                        'Not expected sql string')

    def test_compile_album_search(self):
        album_search = "album : Shaffer"
        expected_sql_search = "SELECT id_rola FROM rolas, albums, performers " \
                            + "WHERE rolas.id_album = albums.id_album " \
                            + "AND rolas.id_performer = performers.id_performer " \
                            + "AND (albums.name LIKE '%Shaffer%')"
        sql_search = self.compiler.compile(album_search)
        self.assertEqual(sql_search, expected_sql_search,
                        'Not expected sql string')

        multiple_album_search = "album  :  Shaffer .  album    :  On The Road  "
        expected_sql_search = "SELECT id_rola FROM rolas, albums, performers " \
                            + "WHERE rolas.id_album = albums.id_album " \
                            + "AND rolas.id_performer = performers.id_performer " \
                            + "AND (albums.name LIKE '%Shaffer%' " \
                            + "OR albums.name LIKE '%On The Road%')"
        sql_search = self.compiler.compile(multiple_album_search)
        self.assertEqual(sql_search, expected_sql_search,
                        'Not expected sql string')

    def test_compile_performer_search(self):
        performer_search = "performer : Andrew Neiman"
        expected_sql_search = "SELECT id_rola FROM rolas, albums, performers " \
                            + "WHERE rolas.id_album = albums.id_album " \
                            + "AND rolas.id_performer = performers.id_performer " \
                            + "AND (performers.name LIKE '%Andrew Neiman%')"
        sql_search = self.compiler.compile(performer_search)
        self.assertEqual(sql_search, expected_sql_search,
                        'Not expected sql string')

        multiple_performer_search = "performer  : Andrew Neiman . " \
                                  + "performer :  Dave Kohl "
        expected_sql_search = "SELECT id_rola FROM rolas, albums, performers " \
                            + "WHERE rolas.id_album = albums.id_album " \
                            + "AND rolas.id_performer = performers.id_performer " \
                            + "AND (performers.name LIKE '%Andrew Neiman%' " \
                            + "OR performers.name LIKE '%Dave Kohl%')"
        sql_search = self.compiler.compile(multiple_performer_search)
        self.assertEqual(sql_search, expected_sql_search,
                        'Not expected sql string')

    def test_compile_genre_search(self):
        genre_search = "genre :  jazz"
        expected_sql_search = "SELECT id_rola FROM rolas, albums, performers " \
                            + "WHERE rolas.id_album = albums.id_album " \
                            + "AND rolas.id_performer = performers.id_performer " \
                            + "AND (genre LIKE '%jazz%')"
        sql_search = self.compiler.compile(genre_search)
        self.assertEqual(sql_search, expected_sql_search,
                        'Not expected sql string')

        multiple_genre_search = "genre  : jazz . " \
                              + "genre :  pop "
        expected_sql_search = "SELECT id_rola FROM rolas, albums, performers " \
                            + "WHERE rolas.id_album = albums.id_album " \
                            + "AND rolas.id_performer = performers.id_performer " \
                            + "AND (genre LIKE '%jazz%' " \
                            + "OR genre LIKE '%pop%')"
        sql_search = self.compiler.compile(multiple_genre_search)
        self.assertEqual(sql_search, expected_sql_search,
                        'Not expected sql string')

    def test_compile_year_search(self):
        year_search = "year :  2014"
        expected_sql_search = "SELECT id_rola FROM rolas, albums, performers " \
                            + "WHERE rolas.id_album = albums.id_album " \
                            + "AND rolas.id_performer = performers.id_performer " \
                            + "AND (rolas.year = 2014)"
        sql_search = self.compiler.compile(year_search)
        self.assertEqual(sql_search, expected_sql_search,
                        'Not expected sql string')

        multiple_year_search = "year  : 2014 . " \
                              + "year :  2012 "
        expected_sql_search = "SELECT id_rola FROM rolas, albums, performers " \
                            + "WHERE rolas.id_album = albums.id_album " \
                            + "AND rolas.id_performer = performers.id_performer " \
                            + "AND (rolas.year = 2014 " \
                            + "OR rolas.year = 2012)"
        sql_search = self.compiler.compile(multiple_year_search)
        self.assertEqual(sql_search, expected_sql_search,
                        'Not expected sql string')

if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestRola)
    except:
        pass
    unittest.TextTestRunner(verbosity=2).run(suite)
