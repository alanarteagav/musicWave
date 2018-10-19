class Rola :
    """Rola class, used to store ID3v2.4 tags, and identifiers related to
       a database."""

    def __init__(self, id, performer_id, album_id, path, title, track, year, genre):
        """Defines a new rola"""
        self.id = id
        self.performer_id = performer_id
        self.album_id = album_id
        self.path = path
        self.title = title
        self.track = track
        self.year = year
        self.genre = genre

    def get_id(self):
        """Returns the rola id"""
        return self.id

    def get_performer_id(self):
        """Returns the rola performer id"""
        return self.performer_id

    def get_album_id(self):
        """Returns the rola album id"""
        return self.album_id

    def get_path(self):
        """Returns the path of the rola"""
        return self.path

    def get_title(self):
        """Returns the title of the rola"""
        return self.title

    def get_track(self):
        """Returns the rola track number"""
        return self.track

    def get_year(self):
        """Returns the year of the rola"""
        return self.year

    def get_genre(self):
        """Returns the genre of the rola"""
        return self.genre

    def set_id(self, id):
        """Sets a new rola id"""
        self.id = id

    def set_performer_id(self, performer_id):
        """Sets a new rola performer id"""
        self.performer_id = performer_id

    def set_album_id(self, album_id):
        """Sets a new rola performer id"""
        self.album_id = album_id

    def set_path(self, path):
        """Sets a new path for the rola"""
        self.path = path

    def set_title(self, title):
        """Sets a new title for the rola"""
        self.title = title

    def set_track(self, track):
        """Sets a new track number for the rola"""
        self.track = track

    def set_year(self, year):
        """Sets a new year for the rola"""
        self.year = year

    def set_genre(self, genre):
        """Sets a new genre for the rola"""
        self.genre = genre
