import os
import os.path
from .rola import Rola
from mutagen.id3 import ID3

class Miner :
    """Miner class, used to read ID3v2.4 tags from mp3 files."""

    def __init__(self, path):
        """Defines a new miner to read ID3v2.4 tags from mp3 files
           in a directory.

           Parameters:
           path (str) : The directory path. """
        self.path = path
        self.rolas = {}
        self.performers = {}
        self.albums = {}
        self.processed_files = 0
        self.paths = []
        self.total_files = 0

        self.rola_count = 1
        self.album_count = 1
        self.artist_count = 1

        self.albums = {}
        self.albums["Unknown"] = 0
        self.performers = {}
        self.performers["Unknown"] = 0
        self.rolas = {}
        self.paths = []

    def setup(self):
        """Method that sets the miner instance variables to default values,
           it is necessary to run before executing the tag mining."""
        self.rolas = {}
        self.performers = {}
        self.albums = {}
        self.processed_files = 0
        self.paths = []
        self.total_files = 0

        self.rola_count = 1
        self.album_count = 1
        self.artist_count = 1

        self.albums = {}
        self.albums["Unknown"] = (0, 0)
        self.performers = {}
        self.performers["Unknown"] = 0
        self.rolas = {}
        self.paths = []

    def walk(self):
        """Method that fills the miner's path list with all the paths
           of the mp3 files which are inside the directory specified in
           the constructor."""
        for root, directories, files in os.walk(self.path):
            for file in files:
                if file.endswith('.mp3'):
                    self.paths.append(os.path.abspath(os.path.join(root, file)))
        self.total_files = len(self.paths)

    def mine(self, path) :
        """Method that retrieves the ID3v2.4 tags from an specific mp3 file,
           and stores them in the miner's dictionaries for rolas, albums
           and performers.

           Parameters:
           path (str) : The mp3 file path. """
        self.processed_files += 1
        audio = ID3(path)

        artist_id = 0
        try:
            artist = audio['TPE1'].text[0]
            if artist in self.performers.keys() :
                artist_id = self.performers[artist]
            else :
                self.performers[artist] = self.artist_count
                artist_id = self.artist_count
                self.artist_count += 1
        except:
            pass

        try:
            year_tag = audio['TDRC'].text[0]
            year_tag = str(year_tag)
            year = int(year_tag)
        except:
            year = 2018

        album_id = 0
        try:
            album = audio['TALB'].text[0]
            if album != [] :
                if str(album) in self.albums.keys() :
                    album_id = self.albums[str(album)][0]
                else :
                    self.albums[str(album)] = (self.album_count, year)
                    album_id = self.album_count
                    self.album_count += 1
        except:
            pass

        try:
            title_tag = audio['TIT2'].text[0]
            title = str(title_tag).replace("'", "´")
        except:
            title = "Unknown"

        try:
            track_tag = audio['TRCK'].text[0]
            track = int(track_tag.split("/")[0])
        except:
            track = 0

        try:
            genre = audio['TCON'].text[0]

        except:
            genre = "Unknown"

        path_string = str(path)
        rola = Rola(id=self.rola_count, performer_id=artist_id,
                    album_id=album_id, path=path_string,
                    title=title, track=track, year=year, genre=genre)
        self.rolas[self.rola_count] = rola
        self.rola_count += 1

    def get_rolas(self) :
        """Method that returns the miner's rolas dictionary, whose keys
           are the id_rola for each rola, and whose values are rola objects.

           Returns: the rolas dictionary."""
        return self.rolas

    def get_performers(self) :
        """Method that returns the miner's performers dictionary, whose keys
           are the name for each performer, and whose values are the
           id_performer for each performer.

           Returns: the performers dictionary."""
        return self.performers

    def get_albums(self) :
        """Method that returns the miner's albums dictionary, whose keys
           are the name for each album, and whose values are the
           id_album for each album.

           Returns: the albums dictionary."""
        return self.albums

    def get_processed_files(self):
        """Method that returns the number of mp3 files that the miner has read
           since the last setup method call.

           Returns: the number of processed mp3 files."""
        return self.processed_files

    def get_total_files(self):
        """Method that returns the number of mp3 files that the miner have to
           read until the next setup method call.

           Returns: the number of mp3 files to process."""
        return self.total_files

    def get_paths(self):
        """Method that returns the list of paths of the mp3 files inside of the
           directory specified in the constructor.

           Returns: list of mp3 files paths."""
        return self.paths
