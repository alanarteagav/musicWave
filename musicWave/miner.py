import os
import os.path
import sqlite3
from mp3_tagger import MP3File, VERSION_2

class miner :
    def create_database():
        connection = sqlite3.connect("music.db")
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE types (
                              id_type INTEGER PRIMARY KEY ,
                              description TEXT
                           )""")
        cursor.execute("""INSERT INTO types VALUES (0 , 'Person ')""")
        cursor.execute("""INSERT INTO types VALUES (1 , 'Group ')""")
        cursor.execute("""INSERT INTO types VALUES (2 , 'Unknown ')""")
        cursor.execute("""CREATE TABLE performers (
                              id_performer INTEGER PRIMARY KEY ,
                              id_type INTEGER ,
                              name TEXT ,
                              FOREIGN KEY ( id_type ) REFERENCES types ( id_type )
                           )""")
        cursor.execute("""CREATE TABLE persons (
                              id_person INTEGER PRIMARY KEY ,
                              stage_name TEXT ,
                              real_name TEXT ,
                              birth_date TEXT ,
                              death_date TEXT
                           )""")
        cursor.execute("""CREATE TABLE groups (
                              id_group INTEGER PRIMARY KEY ,
                              name TEXT ,
                              start_date TEXT ,
                              end_date TEXT
                           )""")
        cursor.execute("""CREATE TABLE albums (
                              id_album INTEGER PRIMARY KEY ,
                              path TEXT ,
                              name TEXT ,
                              year INTEGER
                           )""")
        cursor.execute("""CREATE TABLE rolas (
                              id_rola INTEGER PRIMARY KEY ,
                              id_performer INTEGER ,
                              id_album INTEGER ,
                              path TEXT ,
                              title TEXT ,
                              track INTEGER ,
                              year INTEGER ,
                              genre TEXT ,
                              FOREIGN KEY ( id_performer )
                              REFERENCES performers ( id_performer ) ,
                              FOREIGN KEY ( id_album )
                              REFERENCES albums ( id_album )
                           )""")
        cursor.execute("""CREATE TABLE in_group (
                              id_person INTEGER ,
                              id_group INTEGER ,
                              PRIMARY KEY ( id_person , id_group ) ,
                              FOREIGN KEY ( id_person ) REFERENCES persons ( id_person ) ,
                              FOREIGN KEY ( id_group ) REFERENCES groups ( id_group )
                           )""")
        connection.commit()
        connection.close()

    def populate_database():
        connection = sqlite3.connect("music.db")
        connection.text_factory = str
        cursor = connection.cursor()

        home = os.getenv("HOME")

        album_dict = {}
        artist_dict = {}
        artist_count = 1
        album_count = 1
        id_rola = 1
        for root, directories, files in os.walk(home + "/Music"):
            for file in files:
                if file.endswith('.mp3'):
                    mp3_path = os.path.abspath(os.path.join(root, file))
                    mp3 = MP3File(mp3_path)
                    mp3.set_version(VERSION_2)

                    artist = mp3.artist
                    id_artist = 0
                    if artist != [] :
                        if str(artist) in artist_dict.keys() :
                            id_artist = artist_dict[str(artist)]
                        else :
                            artist_dict[str(artist)] = artist_count
                            id_artist = artist_count
                            cursor.execute('INSERT INTO performers (id_performer, id_type, name) VALUES (?, ?, ?)', (id_artist, 2, str(artist)))
                            artist_count = artist_count + 1

                    album = mp3.album
                    id_album = 0
                    if album != [] :
                        if str(album) in album_dict.keys() :
                            id_album = album_dict[str(album)]
                        else :
                            album_dict[str(album)] = album_count
                            id_album = album_count
                            cursor.execute('INSERT INTO albums ( id_album, name) VALUES (?, ?)', (id_album, str(album)))
                            album_count = album_count + 1

                    song = mp3.song
                    track = mp3.track
                    year = mp3.year
                    genre = mp3.genre
                    path_string = os.path.abspath(os.path.join(root, file))
                    cursor.execute('INSERT INTO rolas ( id_rola, id_performer, id_album, path, title, genre ) VALUES (?, ?, ?, ?, ?, ?)', (id_rola, id_artist, id_album, path_string, song, str(genre)))
                    id_rola = id_rola + 1
        connection.commit()
        connection.close()
