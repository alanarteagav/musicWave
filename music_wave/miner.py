import os
import os.path
from rola import Rola
from mutagen.id3 import ID3

class Miner :

    def __init__(self, path):
        self.path = path
        self.rolas = {}
        self.performers = {}
        self.albums = {}
        self.progress = 0.0

    def mine(self) :
        rola_count = 1
        album_count = 1
        artist_count = 1

        albums = {}
        albums["Unknown"] = 0
        performers = {}
        performers["Unknown"] = 0
        rolas = {}
        paths = []

        for root, directories, files in os.walk(self.path):
            for file in files:
                if file.endswith('.mp3'):
                    paths.append(os.path.abspath(os.path.join(root, file)))

        processed_files = 0
        total_files = len(paths)

        for path in paths:
            processed_files += 1
            self.progress = processed_files * 1.0 / total_files

            audio = ID3(path)

            artist_id = 0
            try:
                artist = audio['TPE1'].text[0]
                if artist in performers.keys() :
                    artist_id = performers[artist]
                else :
                    performers[artist] = artist_count
                    artist_id = artist_count
                    artist_count = artist_count + 1
            except:
                pass


            album_id = 0
            try:
                album = audio['TALB'].text[0]
                if album != [] :
                    if str(album) in albums.keys() :
                        album_id = albums[str(album)]
                    else :
                        albums[str(album)] = album_count
                        album_id = album_count
                        album_count = album_count + 1
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
            rola = Rola(id=rola_count, performer_id=artist_id,
                        album_id=album_id, path=path_string,
                        title=title, track=track, year=year, genre=genre)
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

    def get_progress(self):
        return self.progress
