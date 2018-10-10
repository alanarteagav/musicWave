import os
import os.path
from .rola import Rola
from mp3_tagger import MP3File, VERSION_2

class Miner :

    def __init__(self, path):
        self.path = path
        self.rolas = {}
        self.performers = {}
        self.albums = {}

    def mine(self) :
        rola_count = 1
        album_count = 1
        artist_count = 1

        albums = {}
        performers = {}
        rolas = {}

        for root, directories, files in os.walk(self.path):
            for file in files:
                if file.endswith('.mp3'):
                    mp3 = MP3File(os.path.abspath(os.path.join(root, file)))
                    mp3.set_version(VERSION_2)

                    artist = mp3.artist
                    artist_id = 0
                    if artist != [] :
                        if str(artist) in performers.keys() :
                            artist_id = performers[str(artist)]
                        else :
                            performers[str(artist)] = artist_count
                            artist_id = artist_count
                            artist_count = artist_count + 1

                    album = mp3.album
                    album_id = 0
                    if album != [] :
                        if str(album) in albums.keys() :
                            album_id = albums[str(album)]
                        else :
                            albums[str(album)] = album_count
                            album_id = album_count
                            album_count = album_count + 1

                    song = mp3.song
                    track_retrieved = mp3.track
                    track = int(track_retrieved.split("/")[0])
                    year = int(mp3.year)
                    genre = mp3.genre
                    path_string = os.path.abspath(os.path.join(root, file))
                    rola = Rola(id=rola_count, performer_id=artist_id,
                                album_id=album_id, path=path_string,
                                title=song, track=track, year=year, genre=genre)
                    rolas[rola_count] = rola
                    rola_count = rola_count + 1
        self.rolas = rolas
        self.albums = albums
        self.performers = performers

    def get_rolas(self) :
        return self.rolas

    def get_performers(self) :
        return self.performers

    def get_albums(self) :
        return self.albums
