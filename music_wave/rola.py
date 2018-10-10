class Rola :

    def __init__(self, id, performer_id, album_id, path, title, track, year, genre):
        self.id = id
        self.performer_id = performer_id
        self.album_id = album_id
        self.path = path
        self.title = title
        self.track = track
        self.year = year
        self.genre = genre

    def get_id(self):
        return self.id

    def get_performer_id(self):
        return self.performer_id

    def get_album_id(self):
        return self.album_id

    def get_path(self):
        return self.path

    def get_title(self):
        return self.title

    def get_track(self):
        return self.track

    def get_year(self):
        return self.year

    def get_genre(self):
        return self.genre

    def set_id(self, id):
        self.id = id

    def set_performer_id(self, performer):
        self.performer = performer

    def set_album_id(self, album_id):
        self.album_id = album_id

    def set_path(self, path):
        self.path = path

    def set_title(self, title):
        self.title = title

    def set_track(self, track):
        self.track = track

    def set_year(self, year):
        self.year = Year

    def set_genre(self, genre):
        self.genre = genre
