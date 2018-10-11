import os
import os.path
from rola import Rola
from mp3_tagger import MP3File, VERSION_2
import mutagen
from mutagen.id3 import ID3
from mutagen.mp3 import MP3

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
        paths = []

        for root, directories, files in os.walk(self.path):
            for file in files:
                if file.endswith('.mp3'):
                    paths.append(os.path.abspath(os.path.join(root, file)))

        print(len(paths))
        for path in paths:
            audio = ID3(path)

            file = mutagen.File(path)
            artwork = file.tags['APIC:'].data
            with open('image.jpg', 'wb') as img:
                img.write(artwork)


            file = MP3(path)

            if file.tags:
                for frame in file.tags.getall("APIC"):
                    print(frame.pprint())

            mp3 = MP3File(path)
            mp3.set_version(VERSION_2)

            artist_id = 0
            artist = mp3.artist
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

            song_retrieved = mp3.song
            if song_retrieved != [] :
                song = str(song_retrieved).replace("'", "´")
            else :
                song = "null"

            track_retrieved = mp3.track
            if track_retrieved != [] :
                track = int(track_retrieved.split("/")[0])
            else :
                track = 0

            year_retrieved = mp3.year
            if year_retrieved != [] :
                try:
                    year = int(mp3.year)
                except:
                    year = 2018
            else :
                year = 2018
            genre = mp3.genre
            path_string = str(path)
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
