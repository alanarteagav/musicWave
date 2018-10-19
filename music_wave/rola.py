class Rola :
    """Rola class, used to store ID3v2.4 tags, and identifiers related to
       a database."""

    def __init__(self, id, performer_id, album_id, path, title, track, year, genre):
        """Defines a new rola.

            Parameters:

            id (int) : the identifier for the rola.

            performer_id (int) : the identifier for the performer of the rola.

            album_id (int) : the identifier for the album of the rola.

            path (str) : the path of the mp3 file.

            title (str) : the title of the rola.

            track (int) : the track number of the rola.

            year (int) : the year of the rola.

            genre (str) : the genre of the rola.
            """
        self.id = id
        self.performer_id = performer_id
        self.album_id = album_id
        self.path = path
        self.title = title
        self.track = track
        self.year = year
        self.genre = genre

    def get_id(self):
        """Returns : the rola id (int)"""
        return self.id

    def get_performer_id(self):
        """Returns : the rola performer id (int)"""
        return self.performer_id

    def get_album_id(self):
        """Returns : the rola album id (int)"""
        return self.album_id

    def get_path(self):
        """Returns : the path of the rola (str)"""
        return self.path

    def get_title(self):
        """Returns : the title of the rola (str)"""
        return self.title

    def get_track(self):
        """Returns : the rola track number (int)"""
        return self.track

    def get_year(self):
        """Returns : the year of the rola (int)"""
        return self.year

    def get_genre(self):
        """Returns : the genre of the rola (str)"""
        return self.genre

    def set_id(self, id):
        """Sets a new rola id

            Parameter : id (str) : the identifier for the rola."""
        self.id = id

    def set_performer_id(self, performer_id):
        """Parameter : performer_id (int) : the identifier of the
           rola performer"""
        self.performer_id = performer_id

    def set_album_id(self, album_id):
        """Parameter : album_id (int) : the indentifier of the rola's album."""
        self.album_id = album_id

    def set_path(self, path):
        """Parameter : path (str) : the path of the mp3 file."""
        self.path = path

    def set_title(self, title):
        """Parameter : title (str) : the title of the rola."""
        self.title = title

    def set_track(self, track):
        """Parameter : track (int) : the track number of the rola."""
        self.track = track

    def set_year(self, year):
        """Parameter : year (int) : the year of the rola."""
        self.year = year

    def set_genre(self, genre):
        """Parameter : genre (int) : the genre of the rola."""
        self.genre = genre
