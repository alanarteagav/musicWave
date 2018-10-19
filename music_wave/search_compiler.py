class SearchCompiler :
    """SearchCompiler class, used to compile a defined language to make searches
       in the musicWave program into sql strings."""

    def __init__(self):
        "Constructor, does not receive any parameters."
        self.search_fields = {"album" : [],
                              "performer" : [],
                              "title" : [],
                              "year" : [],
                              "genre" : [],
                              "t" : "title",
                              "a" : "album",
                              "p" : "performer",
                              "y" : "year",
                              "g" : "genre"}
        self.multiple_sentences = True

    def compile(self, string):
        """Method that receives a string of the defined search language for the
           program, and compiles it into a sql string.

           Parameter : string (str) : the string of the defined language.

           Returns : the sql string (str)."""
        instructions = string.split('.')
        for instruction in instructions:
            if instruction.isspace():
                pass
            else :
                field_and_search = instruction.split(":")
                if len(field_and_search) == 1:
                    search = field_and_search[0]
                    self.search_fields["album"].append(search)
                    self.search_fields["performer"].append(search)
                    self.search_fields["title"].append(search)
                    self.multiple_sentences = False

                elif len(field_and_search) == 2:
                    field = field_and_search[0].lower().strip()
                    search = field_and_search[1].strip()
                    if field in self.search_fields :
                        if field == "album" or field == "a" :
                            self.search_fields["album"].append(search)
                        elif field == "performer" or field == "p" :
                            self.search_fields["performer"].append(search)
                        elif field == "title" or field == "t" :
                            self.search_fields["title"].append(search)
                        elif field == "year" or field == "y" :
                            self.search_fields["year"].append(search)
                        elif field == "genre" or field == "g" :
                            self.search_fields["genre"].append(search)

        sql_string = "("
        if len(self.search_fields["title"]) > 0:
            if len(self.search_fields["title"]) == 1:
                title = self.search_fields["title"][0]
                sql_string += "title LIKE '%{}%'".format(title)
            else:
                for index, title in enumerate(self.search_fields["title"]):
                    if index == len(self.search_fields["title"]) - 1:
                        sql_string += "title LIKE '%{}%'".format(title)
                    else:
                        sql_string += "title LIKE '%{}%' OR ".format(title)
            sql_string += ")"
        if len(self.search_fields["album"]) > 0:
            if sql_string != "(":
                if self.multiple_sentences:
                    sql_string += " AND ("
                else :
                    sql_string += " OR ("
            if len(self.search_fields["album"]) == 1:
                album = self.search_fields["album"][0]
                sql_string += "albums.name LIKE '%{}%'".format(album)
            else:
                for index, album in enumerate(self.search_fields["album"]):
                    if index == len(self.search_fields["album"]) - 1:
                        sql_string += "albums.name LIKE '%{}%'".format(album)
                    else:
                        sql_string += "albums.name LIKE '%{}%' OR ".format(album)
            sql_string += ")"
        if len(self.search_fields["performer"]) > 0:
            if sql_string != "(":
                if self.multiple_sentences:
                    sql_string += " AND ("
                else :
                    sql_string += " OR ("
            if len(self.search_fields["performer"]) == 1:
                performer = self.search_fields["performer"][0]
                sql_string += "performers.name LIKE '%{}%'".format(performer)
            else:
                for index, performer in enumerate(self.search_fields["performer"]):
                    if index == len(self.search_fields["performer"]) - 1:
                        sql_string += "performers.name LIKE '%{}%'".format(performer)
                    else:
                        sql_string += "performers.name LIKE '%{}%' OR ".format(performer)
            sql_string += ")"
        if len(self.search_fields["year"]) > 0:
            if sql_string != "(":
                if self.multiple_sentences:
                    sql_string += " AND ("
                else :
                    sql_string += " OR ("
            if len(self.search_fields["year"]) == 1:
                year = self.search_fields["year"][0]
                sql_string += "rolas.year = {}".format(year)
            else:
                for index, year in enumerate(self.search_fields["year"]):
                    if index == len(self.search_fields["year"]) - 1:
                        sql_string += "rolas.year = {}".format(year)
                    else:
                        sql_string += "rolas.year = {} OR ".format(year)
            sql_string += ")"
        if len(self.search_fields["genre"]) > 0:
            if sql_string != "(":
                if self.multiple_sentences:
                    sql_string += " AND ("
                else :
                    sql_string += " OR ("
            if len(self.search_fields["genre"]) == 1:
                genre = self.search_fields["genre"][0]
                sql_string += "genre LIKE '%{}%'".format(genre)
            else:
                for index, genre in enumerate(self.search_fields["genre"]):
                    if index == len(self.search_fields["genre"]) - 1:
                        sql_string += "genre LIKE '%{}%'".format(genre)
                    else:
                        sql_string += "genre LIKE '%{}%' OR ".format(genre)
            sql_string += ")"


        # Clear the dicts.
        self.search_fields["album"].clear()
        self.search_fields["performer"].clear()
        self.search_fields["title"].clear()
        self.search_fields["year"].clear()
        self.search_fields["genre"].clear()

        sql_string = "SELECT id_rola FROM rolas, albums, performers " + \
                     "WHERE rolas.id_album = albums.id_album AND " + \
                     "rolas.id_performer = performers.id_performer AND " + \
                     sql_string
        return sql_string
