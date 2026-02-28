from database.Database import Database

class IGDBGenresDatabase(Database):
    def __init__(self, folder_path: str):
        schema = """
        genre_id INTEGER,
        genre_name TEXT NOT NULL,
        PRIMARY KEY (genre_id),
        UNIQUE (genre_name)
        """

        super().__init__(folder_path=folder_path,
                         table_name="igdb_genres",
                         schema=schema)

    def add_genre(self,genre_name: str) -> int:
        """
        Adds a genre to the database and returns the created genre_id.
        :param genre_name: The name of the genre to be added to the database.
        :returns: The genre_id of the newly added genre.
        """
        query = f"INSERT INTO {self.table_name} (genre_name) VALUES (?)"
        self.sql_execute(query, (genre_name,))

        query = f"SELECT genre_id FROM {self.table_name} WHERE genre_name = ?"
        result = self.sql_execute_fetchall(query, (genre_name,))
        return result[0][0] if result else None

    def genre_exists(self, genre_name: str) -> int | None:
        """
        Checks if a genre with the given genre_name already exists in the database.
        If the genre exists, returns the genre_id. Otherwise, returns None.
        :param genre_name: The name of the genre to check for existence.
        :return: The genre_id of the genre if it exists in the database, None otherwise.
        """
        query = f"SELECT genre_id FROM {self.table_name} WHERE genre_name = ?"
        result = self.sql_execute_fetchall(query, (genre_name,))

        if len(result) == 0:
            return None

        return result[0][0]

    def print_database(self):
        pass