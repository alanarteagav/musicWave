import os
import os.path
from .rola import Rola
from mutagen.id3 import ID3

class Miner :

    def __init__(self, path):
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

    def walk(self):
        for root, directories, files in os.walk(self.path):
            for file in files:
                if file.endswith('.mp3'):
                    self.paths.append(os.path.abspath(os.path.join(root, file)))
        self.total_files = len(self.paths)

    def mine(self, path) :
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

        album_id = 0
        try:
            album = audio['TALB'].text[0]
            if album != [] :
                if str(album) in self.albums.keys() :
                    album_id = self.albums[str(album)]
                else :
                    self.albums[str(album)] = self.album_count
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
            year_tag = audio['TDRC'].text[0]
            year = int(year_tag)
        except:
            year = 2018

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
        return self.rolas

    def get_performers(self) :
        return self.performers

    def get_albums(self) :
        return self.albums

    def get_processed_files(self):
        return self.processed_files

    def get_total_files(self):
        return self.total_files

    def get_paths(self):
        return self.paths
